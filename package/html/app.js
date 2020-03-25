
let todoItems = [];

const todoList = document.querySelector('.js-todo-list')
if(!todoList) {
    console.log('No todo list selected')
}

const form = document.querySelector('.js-form')
if(!form) {
    console.log('No form selected')
}

function addTodo(text) {
    const todo = {
        text: text,
        checked: false,
        id: Date.now()
    };

    todoItems.push(todo);

    let args = {
        id:todo.id,
        text:todo.text,
        checked:todo.checked
    };

    // Save it in redis
    packageGedisClient.mybot.cl.actors.cl.create_note(args).then((resp) => {
        if (resp.ok) {
            resp.json().then((json) => {
                console.log(json.data) 
            })
        } else {
            let err = new Error(resp)
            lastError = err;
            throw err;
        }
    })

    // Create new todo-item li
    todoList.insertAdjacentHTML('beforeend', `
        <li class="todo-item" data-key="${todo.id}">
            <label for="${todo.id}" class="tick js-tick"></label>
            <input id="${todo.id}" type="checkbox"/>
            <label id="todo-label-text">${todo.text}</label>
            <input id="todo-edit-text" type="text" value="${todo.text}">
            <button class="edit-todo js-edit-todo">
                <svg><use href="#edit-icon"></use></svg>
            </button>
            <button class="delete-todo js-delete-todo">
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
            id:todo.id,
            text:todo.text,
            checked:todo.checked
        };

        // Update note in redis
        packageGedisClient.mybot.cl.actors.cl.edit_note(args).then((resp) => {
            if (resp.ok) {
                resp.json().then((json) => {
                    console.log(json.data) 
                })
            } else {
                let err = new Error(resp)
                lastError = err;
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
    if (todoItems.length === 0) todoList.innerHTML = '';

    // Delete note from redis
    let args = {id:Number(key)};
    packageGedisClient.mybot.cl.actors.cl.delete_note(args).then((resp) => {
        if (resp.ok) {
            resp.json().then((json) => {
                console.log(json.data) 
            })
        } else {
            let err = new Error(resp)
            lastError = err;
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

// Navigate between page tabs
function navigate(evt, tab) {

    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Show the current tab, and add an "active" class to the button that opened it
    tabDiv = document.getElementById(tab)
    tabDiv.style.display = "block";
    evt.currentTarget.className += " active";

    // If process tab is clicked, call ps actor to get proc-list
    if(tab == 'proc-tab') {
        packageGedisClient.mybot.cl.actors.cl.ps().then((resp) => {
            if (resp.ok) {
                resp.json().then((json) => {

                    // Create html table to view proc-list
                    var cols = 0;
                    var tableContent =
                    `<h2>Running Processes</h2><hr>
                    <div> 
                        <table class="table table-responsive table-striped table-hover">
                            <thead>
                                <tr>`

                    lines = json.data.split('\n')
                    for (var i in lines) {
                        if( i == 0) {
                            lines[i] = lines[i].replace(/\s+/g,' ').split(' ')
                            for (var word in lines[i]) {
                                tableContent += "<th>" + lines[i][word] + "</th>"
                                cols++;
                            }
                            tableContent +=
                            `   </tr>
                            </thead>
                            <tbody>`
                        }
                        else {
                            tableContent +=
                            `   </tr>`
                            lines[i] = lines[i].replace(/\s+/g,' ').split(' ')
                            for (var word in lines[i]) {
                                if(word == cols - 1) {
                                    tableContent += "<td>" + lines[i].slice(word) + "</td>"
                                    break;
                                }
                                else {
                                    tableContent += "<td>" + lines[i][word] + "</td>"
                                }
                            }
                            tableContent +=
                            `   </tr>`
                        }
                    }

                    tableContent +=
                    `       </tbody>
                        </table>
                    </div>`
                    
                    // Update div with the table
                    tabDiv.innerHTML = tableContent
                })
            } else {
                let err = new Error(resp)
                lastError = err;
                throw err;
            }
        })
    }
}

form.addEventListener('submit', event => {
    event.preventDefault();
    const input = document.querySelector('.js-todo-input');
    const text = input.value.trim();
    if (text !== '') {
        addTodo(text);
        input.value = '';
        input.focus();
    }
    else {
        alert("Empty Note!")
    }
});

todoList.addEventListener('click', event => {
    if (event.target.classList.contains('js-tick')) {
        const itemKey = event.target.parentElement.dataset.key;
        toggleDone(itemKey);
    }

    if (event.target.classList.contains('js-edit-todo')) {
        const itemKey = event.target.parentElement.dataset.key;
        editTodo(itemKey);
    }

    if (event.target.classList.contains('js-delete-todo')) {
        const itemKey = event.target.parentElement.dataset.key;
        deleteTodo(itemKey);
    }
});