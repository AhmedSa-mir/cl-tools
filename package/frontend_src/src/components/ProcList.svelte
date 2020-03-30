<script >
    import { onMount } from 'svelte';
    
    let pageDiv;

    // Create html table to view running-proc-list
    function createTable(json) {

        var cols = 0;
        var tableContent =
        `<h2>Running Processes</h2><hr>
        <div> 
        <table class="table table-responsive table-striped table-hover">
        <thead>
        <tr>`

        var lines = json.data.split('\n')
        for (var i in lines) {

            // Table header
            if(i == 0) {
                
                // Remove whitespaces
                lines[i] = lines[i].replace(/\s+/g,' ').split(' ')
                lines[i] = lines[i].slice(1)

                for (var word in lines[i]) {
                    tableContent += "<th>" + lines[i][word] + "</th>"
                    cols++;
                }
                tableContent += `</tr>
                                </thead>
                                <tbody>`
            }
            else {
                tableContent += `</tr>`

                // Remove whitespaces
                lines[i] = lines[i].replace(/\s+/g,' ').split(' ')
                lines[i] = lines[i].slice(1)

                for (var word in lines[i]) {
                    // last column has many words with spaces in between
                    if(word == cols - 1) {
                        tableContent += "<td>" + lines[i].slice(word) + "</td>"
                        break;
                    }
                    else {
                        tableContent += "<td>" + lines[i][word] + "</td>"
                    }
                }
                tableContent += `</tr>`
            }
        }

        tableContent += `</tbody>
                        </table>
                        </div>`
        
        return tableContent
    }

    onMount(() => {

        // Get running processes
        packageGedisClient.mybot.cli.actors.cli.ps().then((resp) => {
            if (resp.ok) {
                resp.json().then((json) => {

                    // Update div with the table
                    const tableContent = createTable(json)
                    pageDiv.innerHTML = tableContent
                })
            } else {
                let err = new Error(resp)
                lastError = err;
                throw err;
            }
        })
    });
</script>

<div class='proclistpage' bind:this={pageDiv}><p></p></div>

<style>
</style>