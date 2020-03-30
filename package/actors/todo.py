
from Jumpscale import j

import sys
from os import path
sys.path.append(path.dirname( path.dirname(path.abspath(__file__) ) ))
from dbi.ri import ri
from dbi.bcdbi import bcdbi

class todo(j.baseclasses.threebot_actor):
    
    def _init(self, **kwargs):
        # Config database (bcdb || redis)
        kwargs = self.package.install_kwargs
        if 'bcdb' in kwargs and kwargs['bcdb'] == True:
            self.db = bcdbi(self.package.bcdb)
        else:
            self.db = ri()

    @j.baseclasses.actor_method
    def create(self, note_id, text, checked=False,schema_out=None, user_session=None):
        """
        ```in
        note_id = (I)           #id of the todo-note
        text = (S)              #text of the note
        checked = False (B)     #status of the message
        ```

        ```out
        out = (O) !zerobot.todo.resp.1
        ```
        """
        
        try:
            noteid = self.db.note_create(note_id, text, checked)
            return j.data.serializers.json.dumps({'data':noteid})
        except Exception as e:
            return j.data.serializers.json.dumps({'data': str(e)})


    
    @j.baseclasses.actor_method
    def read(self, note_id, schema_out=None, user_session=None):
        """
        ```in
        note_id = (I)           #id of the todo-note
        ```

        ```out
        out = (O) !zerobot.todo.note.1
        ```
        """
        
        try:
            note = self.db.note_read(note_id)
            return j.data.serializers.json.dumps({'data':note})
        except Exception as e:
            return j.data.serializers.json.dumps({'data': str(e)})
    

    @j.baseclasses.actor_method
    def update(self, note_id, text, checked=False, schema_out=None, user_session=None):
        """
        ```in
        note_id = (I)           #id of the todo-note
        text = (S)              #text of the note
        checked = False (B)     #status of the message
        ```

        ```out
        out = (O) !zerobot.todo.resp.1
        ```
        """

        try:
            noteid = self.db.note_update(note_id, text, checked)
            return j.data.serializers.json.dumps({'data':noteid})
        except Exception as e:
            return j.data.serializers.json.dumps({'data': str(e)})

    @j.baseclasses.actor_method
    def delete(self, note_id, schema_out=None, user_session=None):
        """
        ```in
        note_id = (I)    #id of the todo-note
        ```

        ```out
        out = (O) !zerobot.todo.resp.1
        ```
        """

        try:
            noteid = self.db.note_delete(note_id)
            return j.data.serializers.json.dumps({'data':noteid})
        except Exception as e:
            return j.data.serializers.json.dumps({'data': str(e)})