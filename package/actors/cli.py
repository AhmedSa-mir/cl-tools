
from Jumpscale import j

class cli(j.baseclasses.threebot_actor):

    @j.baseclasses.actor_method
    def ps(self, name=None, exists=False, pid=False,
           schema_out=None, user_session=None):
        """
        ps command using JSX SALS
        ```in
        name = None (S)     #name of the process
        exists = False (B)  #flag to check process exists or not
        pid = False (B)     #flag to get pid of the process 
        ```

        ```out
        out = (O) !zerobot.todo.resp.1
        ```
        """
        
        out = ''
        if not any([name, exists, pid]):
            rc, out, err = j.sal.process.execute("ps ax", showout=False)
            return j.data.serializers.json.dumps({'data': out})
        elif not name:
            return j.data.serializers.json.dumps( \
                {'data': 'No process name provided'})
        else:
            if exists:
                out += f'Exists={str(j.sal.process.psfind(name))}\n'
            if pid:
                out += f'PID={str(j.sal.process.getProcessPid(name))}\n'
        
        return j.data.serializers.json.dumps({'data': out})

    @j.baseclasses.actor_method
    def netcheck(self, port=None, info=False, ni=None, hostname=False,
                 ping=None, schema_out=None, user_session=None):
        """
        netstat command using JSX SALS
        ```in
        port = None (I)         #port number to be checked (Listened on or not)
        info = False (B)        #flag to get network interfaces info
        ni = None (S)           #name of the interface whose IP is needed
        hostname = False (B)    #flag to get hostname
        ping = None (S)         #name of the host/IP to be pinged
        ```

        ```out
        out = (O) !zerobot.todo.resp.1
        ```
        """
        
        if port:
            out = j.sal.nettools.checkListenPort(int(port))
        elif ni:
            out = j.sal.nettools.getIpAddress(ni)
        elif hostname:
            out = j.sal.nettools.getHostname()
        elif ping:
            ip = j.sal.nettools.getHostByName(ping)
            out = j.sal.nettools.pingMachine(ip)
        else:
            out = j.sal.nettools.networkinfo_get()
        
        return j.data.serializers.json.dumps({'data': out})
    
    @j.baseclasses.actor_method
    def wordcount(self, path=None, lines=False, words=False, chars=False,
                  schema_out=None, user_session=None):
        """
        wc command using JSX SALS
        ```in
        path = None (S)      #path of the file
        lines = False (B)    #flag to get number of lines or not
        words = False (B)    #flag to get number of words or not
        chars = False (B)    #flag to get number of chars or not
        ```

        ```out
        out = (O) !zerobot.todo.resp.1
        ```
        """
        
        if not path:
            return j.data.serializers.json.dumps( \
                {'data':'No file path provided'})

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

        return j.data.serializers.json.dumps({'data': out})