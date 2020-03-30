
from Jumpscale import j

class ri():
    
    def __init__(self):
        self.redisclient = j.clients.redis.get()

    def note_exists(self, note_id):
        return self.redisclient.hexists('note:'+str(note_id), 'checked')


    def note_create(self, note_id, text, checked=False):
        
        print("ri create")
        out=''
        exists = self.note_exists(note_id)
        if exists:
            raise ValueError(f"Note with id {note_id} already exists")
        else:
            out = self.redisclient.hmset( \
                'note:'+str(note_id), {'checked':str(checked), 'text': text})

        return note_id


    def note_read(self, note_id):
        
        out=''
        exists = self.note_exists(note_id)
        if not exists:
            raise ValueError(f"No note exists with id {note_id}")
        else:
            out = self.redisclient.hmset( \
                'note:'+str(note_id), {'checked':str(checked), 'text': text})

        return out
    

    def note_update(self, note_id, text, checked=False):

        out=''
        exists = self.note_exists(note_id)
        if not exists:
            raise ValueError(f"No note exists with id {note_id}")
        else:
            out = self.redisclient.hmset( \
                'note:'+str(note_id), {'checked':str(checked), 'text': text})

        return note_id


    def note_delete(self, note_id):

        exists = self.note_exists(note_id)
        if not exists:
            raise ValueError(f"No note exists with id {note_id}")
        else:
            out = self.redisclient.hdel('note:'+str(note_id), 'checked', 'text')

        return note_id