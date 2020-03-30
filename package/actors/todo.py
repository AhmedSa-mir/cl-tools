
from Jumpscale import j

class todo(j.baseclasses.threebot_actor):
    
    def _init(self, **kwargs):
        # self.redisclient = j.clients.redis.get()
        self.note_model = self.package.bcdb.model_get(url='zerobot.todo.note.1')

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
        
        out=''
        # exists = self.redisclient.hexists('note:'+str(note_id), 'checked')
        # if exists:
        note = self.note_model.find(noteid=note_id)
        if note:
            return j.data.serializers.json.dumps( \
                {'data': 'Note with ID '+str(note_id)+' exists!'})
        else:
            # out = self.redisclient.hmset( \
                # 'note:'+str(note_id), {'checked':str(checked), 'text': text})
            note = self.note_model.new()
            note.noteid = note_id
            note.text = text
            note.checked = checked
            out = self.note_model.set(note)
            #TODO: check for set output

        return j.data.serializers.json.dumps({'data':out.noteid})


    
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
        
        # exists = self.redisclient.hexists('note:'+str(note_id), 'checked')
        # if not exists:
        note = self.note_model.find(noteid=note_id)
        if not note:
            return j.data.serializers.json.dumps( \
                {'data': 'Note with ID '+str(note_id)+' does not exist!'})
        else:
            # out = self.redisclient.hmset( \
                # 'note:'+str(note_id), {'checked':str(checked), 'text': text})
            out= { \
                'id' : note[0].noteid,
                'text' : note[0].text,
                'checked' : note[0].checked  \
            }

        return j.data.serializers.json.dumps({'data':out})
    

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

        out=''
        # exists = self.redisclient.hexists('note:'+str(note_id), 'checked')
        # if not exists:
        note = self.note_model.find(noteid=note_id)
        if not note:
            return j.data.serializers.json.dumps( \
                {'data': 'Note with ID '+str(note_id)+' does not exist!'})
        else:
            # out = self.redisclient.hmset( \
                # 'note:'+str(note_id), {'checked':str(checked), 'text': text})
            obj = self.note_model.new()
            obj.noteid = note_id
            obj.text = text
            obj.checked = checked
            out = self.note_model.set(obj)
            #TODO: check for set output

        return j.data.serializers.json.dumps({'data':out.noteid})

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

        # exists = self.redisclient.hexists('note:'+str(note_id), 'checked')
        # if not exists:
        note = self.note_model.find(noteid=note_id)
        if not note:
            return j.data.serializers.json.dumps( \
                {'data': 'Note with ID '+str(note_id)+' does not exist!'})
        else:
            # out = self.redisclient.hdel('note:'+str(note_id), 'checked', 'text')
            self.note_model.delete(note[0])
            #TODO: output of delete is None always

        return j.data.serializers.json.dumps({'data':'OK'})