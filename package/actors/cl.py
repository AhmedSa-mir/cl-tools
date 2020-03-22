
from Jumpscale import j

class cl(j.baseclasses.threebot_actor):
    
    @j.baseclasses.actor_method
    def ps(self, name=None, exists=False, pid=False, schema_out=None, user_session=None):
        """
        ps command using JSX SALS
        @param name is name of the process
        @param exists is a flag to check process exists or not
        @param pid is a flag to get pid of the process 
        """

        out = ''

        if not any([name, exists, pid]):
            rc, out, err = j.sal.process.execute("ps ax", showout=False)
            return out
        elif not name:
            return 'No process name provided'
        else:
            if exists:
                out += f'Exists={str(j.sal.process.psfind(name))}\n'
            if pid:
                out += f'PID={str(j.sal.process.getProcessPid(name))}\n'
        
        return out

    @j.baseclasses.actor_method
    def netcheck(self, port=None, info=False, NI=None, hostname=False, ping=None,
                schema_out=None, user_session=None):
        """
        netstat command using JSX SALS
        @param port is port number to be checked (Listened on or not)
        @param info is a flag to get network interfaces info
        @param NI is the name of the interface whose IP is needed
        @param hostname is a flag to get hostname
        @param ping is the name of the host/IP to be pinged
        """
        
        if port:
            out = j.sal.nettools.checkListenPort(int(port))
        elif NI:
            out = j.sal.nettools.getIpAddress(NI)
        elif hostname:
            out = j.sal.nettools.getHostname()
        elif ping:
            ip = j.sal.nettools.getHostByName(ping)
            out = j.sal.nettools.pingMachine(ip)
        else:
            out = j.sal.nettools.networkinfo_get()
        
        return out
    
    @j.baseclasses.actor_method
    def wordcount(self, path=None, lines=False, words=False, chars=False,
                schema_out=None, user_session=None):
        """
        wc command using JSX SALS
        @param path is the path of the file
        @param lines is a flag to get number of lines or not
        @param words is a flag to get number of words or not
        @param chars is a flag to get number of chars or not
        """
        
        if not path:
            return 'No file path provided'

        file_content = j.sal.fs.readFile(path)
        no_options = False
        out = ''

        if not any([lines, words, chars]):
            no_options = True
        if no_options or lines:
            # the trailing 1 is the last line (doesn't have \n at the end)
            lines_cnt = file_content.count('\n') + 1
            out += f'Lines={lines_cnt}\n'
        if no_options or words:
            # the trailing 1 is the last word
            words_cnt = file_content.count(" ") + file_content.count('\n') + 1
            out += f'Words={words_cnt}\n'
        if no_options or chars:
            out += f'Characters={len(file_content)}\n'

        return out