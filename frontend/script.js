 const API = "http://127.0.0.1:8000";


// Load tasks when page opens

window.onload = loadTasks;



async function loadTasks(){

    let response = await fetch(
        API + "/tasks"
    );


    let data = await response.json();


    let list = document.getElementById(
        "taskList"
    );


    list.innerHTML="";


    let tasks = data.tasks;


    tasks.forEach(task=>{


        list.innerHTML += `

        <div class="task-card">


            <div>

                <h3>${task.task}</h3>

                <p class="priority">
                Priority: ${task.priority}
                </p>


                <span class="status 
                ${task.status.toLowerCase()}">

                ${task.status}

                </span>


            </div>



            <div class="actions">


                <button onclick="completeTask('${task.task}')">
                ✅
                </button>


                <button onclick="deleteTask('${task.task}')">
                🗑
                </button>


            </div>


        </div>

        `;


    });


}



async function addTask(){


    let task =
    document.getElementById(
        "taskInput"
    ).value;


    let priority =
    document.getElementById(
        "priority"
    ).value;



    await fetch(
        API+"/add",
        {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },


        body:JSON.stringify({

            task:task,
            priority:priority

        })

        }
    );


    document.getElementById(
        "taskInput"
    ).value="";


    loadTasks();

}




async function completeTask(task){


    await fetch(
        API+"/complete",
        {

        method:"PUT",

        headers:{
            "Content-Type":"application/json"
        },


        body:JSON.stringify({

            task:task

        })

        }
    );


    loadTasks();

}




async function deleteTask(task){


    await fetch(
        API+"/delete",
        {

        method:"DELETE",

        headers:{
            "Content-Type":"application/json"
        },


        body:JSON.stringify({

            task:task

        })

        }
    );


    loadTasks();

}
async function askAgent() {

    let message = document.getElementById("agentInput").value;

    if (message.trim() === "") {
        return;
    }

    let response = await fetch(API + "/agent", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })

    });

    let data = await response.json();

    document.getElementById("response").innerText =
        data.response || data.error;

    document.getElementById("agentInput").value = "";
}