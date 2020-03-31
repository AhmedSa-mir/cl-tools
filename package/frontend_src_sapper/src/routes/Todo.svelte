<script >
    import { onMount } from 'svelte';

    let todoItems = [];
    let listDiv;
    let formDiv;
    let inputDiv;

    onMount(() => {
        
        formDiv.addEventListener('submit', event => {
            event.preventDefault();
            const text = inputDiv.value.trim();
            if (text !== '') {
                addTodo(text);
                inputDiv.value = '';
                inputDiv.focus();
            }
            else {
                alert("Empty Note!")
            }
        });

        listDiv.addEventListener('click', event => {
            if (event.target.classList.contains('todo-tick')) {
                const itemKey = event.target.parentElement.dataset.key;
                toggleDone(itemKey);
            }

            if (event.target.classList.contains('edit-todo')) {
                const itemKey = event.target.parentElement.dataset.key;
                editTodo(itemKey);
            }

            if (event.target.classList.contains('delete-todo')) {
                const itemKey = event.target.parentElement.dataset.key;
                deleteTodo(itemKey);
            }
        });

    });

    function addTodo(text) {
        const todo = {
            text: text,
            checked: false,
            id: Number(String(Date.now()).substring(5))
        };

        todoItems.push(todo);

        let args = {
            note_id:todo.id,
            text:todo.text,
            checked:todo.checked
        };

        // Save it in redis/bcdb
        packageGedisClient.zerobot.todo.actors.todo.create(args).then((resp) => {
            if (resp.ok) {
                resp.json().then((json) => {
                    console.log(json.data) 
                })
            } else {
                let err = new Error(resp)
                throw err;
            }
        })

        // Create new todo-item li
        listDiv.insertAdjacentHTML('beforeend',
        `<li class="todo-item" data-key="${todo.id}">
            <label for="${todo.id}" class="todo-tick"></label>
            <input id="${todo.id}" type="checkbox"/>
            <label id="todo-label-text">${todo.text}</label>
            <input id="todo-edit-text" type="text" value="${todo.text}">
            <button class="edit-todo">
                <svg><use href="#edit-icon"></use></svg>
            </button>
            <button class="delete-todo delete-todo">
                <svg><use href="#delete-icon"></use></svg>
            </button>
        </li>`
        );
    }

    function editTodo(key) {
        const index = todoItems.findIndex(item => item.id === Number(key));
        let todo = todoItems[index];
        const item = document.querySelector(`[data-key='${key}']`);
        var label = item.querySelector("#todo-label-text")
        var editInput = item.querySelector("#todo-edit-text")
        var inEditMode = item.classList.contains("editMode");
    
        if(inEditMode) {

            // Switch from .editMode
            label.innerText = editInput.value;

            let args = {
                note_id:todo.id,
                text:todo.text,
                checked:todo.checked
            };

            // Update note in redis/bcdb
            packageGedisClient.zerobot.todo.actors.todo.update(args).then((resp) => {
                if (resp.ok) {
                    resp.json().then((json) => {
                        console.log(json.data) 
                    })
                } else {
                    let err = new Error(resp)
                    throw err;
                }
            })
        } else {

            // Switch to .editMode
            editInput.value = label.innerText;
        }

        // Toggle .editMode of the item
        item.classList.toggle("editMode");
    }

    function deleteTodo(key) {
        todoItems = todoItems.filter(item => item.id !== Number(key));
        const item = document.querySelector(`[data-key='${key}']`);
        item.remove();

        // Trim all whitespaces once there are no todo items left
        if (todoItems.length === 0) listDiv.innerHTML = '';

        // Delete note from redis/bcdb
        let args = {note_id:Number(key)};
        packageGedisClient.zerobot.todo.actors.todo.delete(args).then((resp) => {
            if (resp.ok) {
                resp.json().then((json) => {
                    console.log(json.data) 
                })
            } else {
                let err = new Error(resp)
                throw err;
            }
        })
    }

    // Toggle done class for the todo-item
    function toggleDone(key) {
        const index = todoItems.findIndex(item => item.id === Number(key));
        todoItems[index].checked = !todoItems[index].checked;

        const item = document.querySelector(`[data-key='${key}']`);
        if (todoItems[index].checked) {
            item.classList.add('done');
        } else {
            item.classList.remove('done');
        }
    }
</script>

<div class='todopage container' id="todo-tab">
    <h1 class="app-title">TODO</h1>
    <ul class="todo-list" bind:this={listDiv}></ul>

    <div class="empty-state">
        <svg class="checklist-icon"><use href="#checklist-icon"></use></svg>
        <h2 class="empty-state-title">Add your first todo</h2>
        <p class="empty-state-description">What do you want to get done today?</p>
    </div>

    <form class="todo-form" bind:this={formDiv}>
        <input type="text" placeholder="e.g: Build a JSX package" class="todo-input" bind:this={inputDiv}>
        <button type="submit" class="add-button">ADD</button>
    </form>
</div>

<svg class="svg-icon">
    <defs>
        <symbol id="checklist-icon" viewBox="-52 0 512 512">
            <path d="m217.140625 47.226562c0 7.1875-5.832031 13.015626-13.019531 13.015626-7.191406 0-13.019532-5.828126-13.019532-13.015626 0-7.191406 5.828126-13.019531 13.019532-13.019531 7.1875 0 13.019531 5.828125 13.019531 13.019531zm0 0"/><path d="m140.917969 98.820312c4.144531 0 7.5-3.355468 7.5-7.5v-11.4375c0-4.140624-3.355469-7.5-7.5-7.5-4.140625 0-7.5 3.359376-7.5 7.5v11.4375c0 4.144532 3.359375 7.5 7.5 7.5zm0 0"/><path d="m267.320312 98.820312c4.144532 0 7.5-3.355468 7.5-7.5v-11.4375c0-4.140624-3.355468-7.5-7.5-7.5-4.140624 0-7.5 3.359376-7.5 7.5v11.4375c0 4.144532 3.359376 7.5 7.5 7.5zm0 0"/><path d="m204.121094 104.925781c8.242187 0 15.984375-3.449219 21.246094-9.464843 2.726562-3.117188 2.40625-7.855469-.710938-10.582032-3.121094-2.726562-7.855469-2.410156-10.582031.710938-2.410157 2.753906-6.039063 4.335937-9.953125 4.335937-3.917969 0-7.542969-1.582031-9.953125-4.335937-2.726563-3.121094-7.464844-3.4375-10.582031-.710938-3.121094 2.726563-3.4375 7.464844-.710938 10.582032 5.257812 6.015624 13 9.464843 21.246094 9.464843zm0 0"/><path d="m162.492188 184.390625c-1.308594-3.929687-5.558594-6.054687-9.484376-4.742187-21.402343 7.132812-37.015624 17.507812-46.878906 25.582031v-9.789063c0-4.140625-3.359375-7.5-7.5-7.5s-7.5 3.359375-7.5 7.5v12.710938c0 11.421875 13.816406 17.8125 22.5 10.359375 8.640625-7.410157 23.304688-17.695313 44.121094-24.636719 3.929688-1.308594 6.054688-5.554688 4.742188-9.484375zm0 0"/><path d="m211.460938 208.035156h98.148437c4.144531 0 7.5-3.359375 7.5-7.5s-3.355469-7.5-7.5-7.5h-98.148437c-4.140626 0-7.5 3.359375-7.5 7.5s3.359374 7.5 7.5 7.5zm0 0"/><path d="m162.492188 245.972656c-1.308594-3.929687-5.558594-6.054687-9.484376-4.746094-21.402343 7.136719-37.015624 17.511719-46.878906 25.585938v-9.789062c0-4.144532-3.359375-7.5-7.5-7.5s-7.5 3.355468-7.5 7.5v12.710937c0 11.40625 13.8125 17.808594 22.5 10.359375 8.640625-7.410156 23.304688-17.699219 44.121094-24.636719 3.929688-1.308593 6.054688-5.554687 4.742188-9.484375zm0 0"/><path d="m211.460938 269.617188h98.148437c4.144531 0 7.5-3.359376 7.5-7.5 0-4.144532-3.355469-7.5-7.5-7.5h-98.148437c-4.140626 0-7.5 3.355468-7.5 7.5 0 4.140624 3.359374 7.5 7.5 7.5zm0 0"/><path d="m162.492188 307.554688c-1.308594-3.929688-5.558594-6.054688-9.484376-4.746094-21.402343 7.136718-37.015624 17.511718-46.878906 25.585937v-9.789062c0-4.144531-3.359375-7.5-7.5-7.5s-7.5 3.355469-7.5 7.5v12.710937c0 11.402344 13.8125 17.808594 22.5 10.359375 8.640625-7.410156 23.308594-17.699219 44.121094-24.636719 3.929688-1.308593 6.054688-5.554687 4.742188-9.484374zm0 0"/><path d="m211.460938 331.199219h98.148437c4.144531 0 7.5-3.359375 7.5-7.5 0-4.144531-3.355469-7.5-7.5-7.5h-98.148437c-4.140626 0-7.5 3.355469-7.5 7.5 0 4.140625 3.359374 7.5 7.5 7.5zm0 0"/><path d="m98.628906 372.6875c-4.140625 0-7.5 3.359375-7.5 7.5v12.710938c0 11.402343 13.808594 17.820312 22.5 10.359374 8.640625-7.410156 23.308594-17.699218 44.121094-24.636718 3.929688-1.308594 6.054688-5.558594 4.746094-9.484375-1.3125-3.933594-5.558594-6.054688-9.488282-4.746094-21.398437 7.132813-37.015624 17.511719-46.878906 25.582031v-9.789062c0-4.140625-3.359375-7.496094-7.5-7.496094zm0 0"/><path d="m211.460938 392.777344h98.148437c4.144531 0 7.5-3.355469 7.5-7.5 0-4.140625-3.355469-7.5-7.5-7.5h-98.148437c-4.140626 0-7.5 3.359375-7.5 7.5 0 4.144531 3.359374 7.5 7.5 7.5zm0 0"/><path d="m369.109375 67.765625h-51.667969v-1.007813c0-13.617187-11.078125-24.695312-24.695312-24.695312h-41.683594c-2.578125-23.621094-22.648438-42.0625-46.941406-42.0625-24.296875 0-44.363282 18.441406-46.945313 42.0625h-41.679687c-13.617188 0-24.695313 11.078125-24.695313 24.695312v1.007813h-51.671875c-21.574218 0-39.128906 17.554687-39.128906 39.128906v48.898438c0 4.140625 3.359375 7.5 7.5 7.5s7.5-3.359375 7.5-7.5v-48.898438c0-13.304687 10.824219-24.128906 24.128906-24.128906h51.671875v18.847656h-43.507812c-4.144531 0-7.5 3.359375-7.5 7.5v345.066407c0 4.140624 3.355469 7.5 7.5 7.5h234.792969c4.144531 0 7.5-3.359376 7.5-7.5 0-4.144532-3.355469-7.5-7.5-7.5h-227.292969v-330.066407h36.472656c.003906.019531.011719.039063.015625.058594.007812.039063.011719.078125.019531.113281 2.320313 11.316406 12.648438 19.726563 24.195313 19.726563h177.25c11.441406 0 21.882812-8.457031 24.191406-19.726563.007812-.035156.015625-.074218.023438-.113281.003906-.019531.007812-.035156.011718-.058594h36.476563v330.066407h-41.359375c-4.144532 0-7.5 3.355468-7.5 7.5 0 4.140624 3.355468 7.5 7.5 7.5h48.859375c4.140625 0 7.5-3.359376 7.5-7.5v-345.066407c0-4.140625-3.359375-7.5-7.5-7.5h-43.507813v-18.847656h51.671875c13.304688 0 24.128907 10.824219 24.128907 24.128906v365.976563c0 13.304687-10.824219 24.128906-24.128907 24.128906h-329.984375c-13.304687 0-24.128906-10.824219-24.128906-24.128906v-287.082032c0-4.140624-3.359375-7.5-7.5-7.5s-7.5 3.359376-7.5 7.5v287.082032c0 21.574218 17.554688 39.128906 39.128906 39.128906h329.980469c21.578125 0 39.128906-17.554688 39.128906-39.128906v-365.976563c.003907-21.574219-17.550781-39.128906-39.128906-39.128906zm-263.308594-1.007813c0-5.347656 4.347657-9.695312 9.695313-9.695312h48.972656c5.792969 0 7.425781-5.015625 7.425781-9.839844 0-17.765625 14.457031-32.222656 32.226563-32.222656 17.765625 0 32.222656 14.453125 32.222656 32.222656 0 4.8125 1.691406 9.839844 7.425781 9.839844h48.976563c5.347656 0 9.695312 4.347656 9.695312 9.695312v42.355469c0 1.875.128906 3.769531-.4375 5.582031-1.226562 3.945313-4.914062 6.816407-9.257812 6.816407h-177.25c-4.34375 0-8.03125-2.871094-9.261719-6.816407-.558594-1.796874-.433594-3.71875-.433594-5.582031zm0 0"/>
        </symbol>
        <symbol id="edit-icon" viewBox="0 0 20 20">
            <path d="M18.303,4.742l-1.454-1.455c-0.171-0.171-0.475-0.171-0.646,0l-3.061,3.064H2.019c-0.251,0-0.457,0.205-0.457,0.456v9.578c0,0.251,0.206,0.456,0.457,0.456h13.683c0.252,0,0.457-0.205,0.457-0.456V7.533l2.144-2.146C18.481,5.208,18.483,4.917,18.303,4.742 M15.258,15.929H2.476V7.263h9.754L9.695,9.792c-0.057,0.057-0.101,0.13-0.119,0.212L9.18,11.36h-3.98c-0.251,0-0.457,0.205-0.457,0.456c0,0.253,0.205,0.456,0.457,0.456h4.336c0.023,0,0.899,0.02,1.498-0.127c0.312-0.077,0.55-0.137,0.55-0.137c0.08-0.018,0.155-0.059,0.212-0.118l3.463-3.443V15.929z M11.241,11.156l-1.078,0.267l0.267-1.076l6.097-6.091l0.808,0.808L11.241,11.156z"></path>
        </symbol>
        <symbol id="delete-icon" viewBox="0 0 20 20">
            <path d="M17.114,3.923h-4.589V2.427c0-0.252-0.207-0.459-0.46-0.459H7.935c-0.252,0-0.459,0.207-0.459,0.459v1.496h-4.59c-0.252,0-0.459,0.205-0.459,0.459c0,0.252,0.207,0.459,0.459,0.459h1.51v12.732c0,0.252,0.207,0.459,0.459,0.459h10.29c0.254,0,0.459-0.207,0.459-0.459V4.841h1.511c0.252,0,0.459-0.207,0.459-0.459C17.573,4.127,17.366,3.923,17.114,3.923M8.394,2.886h3.214v0.918H8.394V2.886z M14.686,17.114H5.314V4.841h9.372V17.114z M12.525,7.306v7.344c0,0.252-0.207,0.459-0.46,0.459s-0.458-0.207-0.458-0.459V7.306c0-0.254,0.205-0.459,0.458-0.459S12.525,7.051,12.525,7.306M8.394,7.306v7.344c0,0.252-0.207,0.459-0.459,0.459s-0.459-0.207-0.459-0.459V7.306c0-0.254,0.207-0.459,0.459-0.459S8.394,7.051,8.394,7.306"></path>
        </symbol>
    </defs>
</svg>

<style>
.container {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
    padding-left: 10px;
    padding-right: 10px;
    color: #333;
    margin-top: 5vh;
    margin-bottom: 5vh;
    overflow-y: auto;
}

:global(.app-title) {
    text-align: center;
    margin-bottom: 20px;
    font-size: 80px;
    opacity: 0.5;
}

:global(.svg-icon) {
    width: 1em;
    height: 1em;
}
  
:global(.svg-icon path,
.svg-icon polygon,
.svg-icon rect) {
    fill: #4691f6;
}
  
:global(.svg-icon circle) {
    stroke: #4691f6;
    stroke-width: 1;
}

:global(.todo-list) {
    list-style: none;
    margin-bottom: 20px;
}

:global(.todo-item) {
    margin-bottom: 10px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

:global(#todo-label-text) {
    flex-grow: 1;
    width: 100%;
    margin-left: 10px;
    margin-right: 10px;
    font-size: 20px;
    overflow: hidden;
    text-overflow: ellipsis;
}

:global(#todo-edit-text) {
    flex-grow: 1;
    margin-left: 10px;
    margin-right: 10px;
    font-size: 15px;
}

:global(.done #todo-label-text) {
    text-decoration: line-through;
}

:global(.todo-tick  ) {
    width: 30px;
    height: 30px;
    border: 3px solid #333;
    border-radius: 50%;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}

:global(.todo-tick::before) {
    content: '✓';
    font-size: 20px;
    display: none;
}

:global(.done .todo-tick::before) {
    display: inline;
}

:global(.delete-todo,
.edit-todo) {
    border: none;
    background-color: transparent;
    outline: none;
    cursor: pointer;
}

:global(.delete-todo svg,
.edit-todo svg) {
    width: 30px;
    height: 30px;
    pointer-events: none;
}

:global(form) {
    width: 100%;
    display: flex;
    justify-content: space-between;
}

:global(.todo-input) {
    width: 100%;
    padding: 10px;
    border-radius: 4px;
    border: 3px solid #333;
}

:global(#todo-edit-text) {
    padding: 4px;
    border-radius: 4px;
    border: 3px solid #333;
}

:global(.add-button) {
    box-shadow:inset 0px 1px 0px 0px #a6827e;
	background:linear-gradient(to bottom, #7d5d3b 5%, #634b30 100%);
	background-color:#7d5d3b;
	border-radius:3px;  
    border:1px solid #54381e;
    color:white;
    padding: 10px 20px;
    margin-left: 5px;
    font-weight: bold;
}

:global(.empty-state) {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    display: none;
}
  
:global(.checklist-icon) {
    margin-bottom: 20px;
}
  
:global(.empty-state-title, .empty-state-description) {
    margin-bottom: 20px;
}

:global(.todo-list:empty) {
    display: none;
}
  
:global(.todo-list:empty + .empty-state) {
    display: flex;
}

:global(#todo-edit-text) {
    display:none;
}
  
:global(ul li.editMode #todo-edit-text) {
    display:block;
}
  
:global(ul li.editMode #todo-label-text) {
    display:none;
}

:global(input[type="checkbox"]) {
    display: none;
}
</style>