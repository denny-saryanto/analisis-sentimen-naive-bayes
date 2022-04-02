$(document).ready( () => {

    getFilesInfo = () => {
        $.ajax({
            url: '/api/file',
            type: 'GET',
            dataType: 'JSON',
            success: (resp) => {
                for(let x=0; x < resp.list_files.length; x++){
                    $("#outputTable > tbody").append("<tr><td>"+resp.list_files[x]+"</td><td>Test</td><td>"+resp.list_files_size[x]+" MB</td></tr>");
                }
                $('#totalFile').text(resp.total_file);
                $('#totalSizeFile').text(resp.total_size_file + ' MB');
            }
        });
    }

    $('#reloadData').click( () => {
        $('#outputTable tbody').remove();
        $('#outputTable').append("<tbody></tbody>");
        getFilesInfo();
    });

    let get_label_select = $('#select_label').find(':selected').text();
    let get_text_select = $('#select_text').find(':selected').text();
    
    if(get_label_select != 'Not Found' && get_text_select != 'Not Found'){
        $('#select_label').removeAttr("disabled");
        $('#select_text').removeAttr("disabled");
        $('#button_submit').removeAttr("disabled");
        $('#get_label').attr("disabled", true);
    } else {
        $('#button_submit').on('click', () => {
            console.log(get_text_select);
            console.log(get_label_select);
        });
    }

    getFilesInfo();
});