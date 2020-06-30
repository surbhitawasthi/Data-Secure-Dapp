$(document).ready(function() {
    // console.log( "ready!" );
    document.getElementById('searchBar').addEventListener('submit', (ev) => {
        ev.preventDefault()
        fetchFunction()
    })

    const downloadAnchor = Array.from(document.getElementsByClassName("downloadFile"))
    downloadAnchor.forEach(function (item) {
        item.addEventListener('click', function(event){
            download_file_func(event,item,false)
        })
    });
});

const download_file_func = function(event,item,search_bar){
    event.preventDefault();
    const user_address = $('#user_add').html().replace('User: ','');
    // console.log(user_address)
    const options = {
        method: 'POST',
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
        body: JSON.stringify({ 'fileName': item.innerHTML, 'user_address': user_address, 'search_bar': search_bar})
    };
    fetch('/download_file',options)
        .then(async (resp) => {
            if (!resp.ok) {
                const responseContent = await resp.json()
                throw responseContent.error
            } else {
                return resp.blob();
            }
        }).then(async (blob) => {
            const url = await window.URL.createObjectURL(blob);
            // For opening in a new tab
            window.open(url,'_blank').focus();
            // For downloading the file
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = item.innerHTML.replace('.enc','');
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch((err) => {
            if(err==='Unauthorised Access'){
                return swal("Oh Nooooo!", err, "error")
            }
            else{
                return swal("Oh Nooooo!", err, "warning")
            }
        });
}

const fetchFunction = async () => {
    const user_address = $('#search_string').val()
    const options = {
        method: 'POST',
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
        body: JSON.stringify({ 'searchString': user_address })
    };
    try{
        const response = await fetch('/search',options)
        if(response.status !== 200){
            const responseJSON = await response.json()
            $('#search_string').val('');
            return swal("NO TRESPASSING", responseJSON['error'], "error");
        }
        const responseJSON = await response.json()
        var i, content;
        var tableOfFiles = $('#tableFile');
        tableOfFiles.empty();
        for(i=0; i<responseJSON.length; i++){
            content = '<tr><th>' + (i+1) + '</th><td><a href="" class="downloadFileSearchbar">' + responseJSON[i]['filename'] + '</a></td></tr>';
            tableOfFiles.append(content);
        }

        $('#user_add').html('User: '+user_address);

        // Show the modal now
        $('#filesPatients').modal('show');

        // Event Listener add karo
        const downloadAnchor = Array.from(document.getElementsByClassName("downloadFileSearchbar"))
        downloadAnchor.forEach(function(item) {
            item.addEventListener('click', function(event){
                download_file_func(event,item,true)
            })
        });

        $('#search_string').val('');
    } catch(error){
        console.log(error)
    }
}