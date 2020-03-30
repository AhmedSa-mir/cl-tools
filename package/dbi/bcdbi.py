
from Jumpscale import j

class bcdbi():
    
    def __init__(self, bcdb):
        self.note_model = bcdb.model_get(url='zerobot.todo.note.1')

    def note_exists(self, note_id):
        return self.note_model.find(noteid=note_id)

    def note_create(self, note_id, text, checked=False):
    
        out=''
        note = self.note_exists(note_id)
        if note:
            raise ValueError(f"Note with id {note_id} already exists")
        else:
            note = self.note_model.new()
            note.noteid = note_id
            note.text = text
            note.checked = checked
            out = self.note_model.set(note)
            #TODO: check for set output

        return note_id

    def note_read(self, note_id):
        
        note = self.note_exists(note_id)
        if not note:
            raise ValueError(f"No note exists with id {note_id}")
        else:
            out= { \
                'id' : note[0].noteid, \
                'text' : note[0].text, \
                'checked' : note[0].checked \
            }

        return out
    

    def note_update(self, note_id, text, checked=False):

        out=''
        note = self.note_exists(note_id)
        if not note:
            raise ValueError(f"No note exists with id {note_id}")
        else:
            obj = self.note_model.new()
            obj.noteid = note_id
            obj.text = text
            obj.checked = checked
            out = self.note_model.set(obj)
            #TODO: check for set output

        return note_id


    def note_delete(self, note_id):

        note = self.note_exists(note_id)
        if not note:
            raise ValueError(f"No note exists with id {note_id}")
        else:
            self.note_model.delete(note[0])
            #TODO: output of delete is None always

        return note_id