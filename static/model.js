$(document).ready( () => {

    getModelInfo = () => {
        $.ajax({
            url: '/api/model/info',
            type: 'GET',
            dataType: 'JSON',
            success: (resp) => {
                $('#td_model_name').text(resp.model_name);
                $('#td_model_date').text(resp.data_time);
                $('#td_tfidf_name').text(resp.tfidf_name);
                $('#td_tfidf_date').text(resp.data_time);
                $('#modelAccuracy').text(resp.model_reports.accuracy_score);
                $('#modelPrecision').text(resp.model_reports.precision_score);
                $('#modelRecall').text(resp.model_reports.recall_score);
                $('#modelF1score').text(resp.model_reports.f1_score);
            }
        });
    }

    getConfusionMatrix = () => {
        $.ajax({
            url: '/api/model/info',
            type: 'GET',
            dataType: 'JSON',
            success: (resp) => {
                data_json = resp.model_reports.cfm;
                label = null;
                for(x=0; x<3; x++){
                    if(x == 0){
                        label = 'positif'
                    } else if (x == 1){
                        label = 'netral'
                    } else {
                        label = 'negatif'
                    }
                    $('#body_cfm').append('<tr><td><strong>'+label+'</strong></td><td>'+data_json[x][0]+'</td><td>'+data_json[x][1]+'</td><td>'+data_json[x][2]+'</td></tr>');
                }
            }
        });
    }

    getTop10Words = (label, value, id) => {
        let chart = new Chart($(id)[0].getContext('2d'), {
            type: 'pie',
            data: {
                labels: label,
                datasets: [{
                    data: value,
                    backgroundColor : color,
                }]
            },
            options: {
                legend: { 
                    display: true 
                },
                maintainAspectRatio : false,
                responsive : true,
            }
        });
    }

    $('#btn_text_predict').on('click', () => {
        if($('#input_text_predict').val() == null || $('#input_text_predict').val() == ''){
            Swal.fire({
                title: 'Text Not Found',
                icon: 'error',
                showCloseButton: true,
                showConfirmButton: false,
                allowEscapeKey: false,
                allowOutsideClick: false,
            });
        } else {
            $.ajax({
                url: '/api/predict',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    type: 'text',
                    input_text : $('#input_text_predict').val(),
                    model_name : 'model.pickle',
                    tfidf_name : 'tfidf.pickle'
                }),
            }).done( (resp) => {
                Swal.fire({
                    title: resp.result,
                    icon: 'info',
                    showConfirmButton: false,
                    showCloseButton: true,
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                });
            });
        }
    });

    $('#btn_file_predict').on('click', () => {
        if($('#input_file_predict')[0].files.length === 0){
            Swal.fire({
                title: 'File Not Found',
                icon: 'error',
                showCloseButton: true,
                showConfirmButton: false,
                allowEscapeKey: false,
                allowOutsideClick: false,
            });
        } else {
            form_data = new FormData($('#upload_file')[0]);
            Swal.fire({
                title: 'Classifying...',
                icon: 'info',
                allowEscapeKey: false,
                allowOutsideClick: false,
                onOpen: () => {
                    swal.showLoading();
                }
            });
            $.ajax({
                url: '/api/predict/file',
                type: 'POST',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
            }).done( (resp) => {
                Swal.close();
                Swal.fire({
                    title: resp.result,
                    icon: 'success',
                    showCloseButton: true,
                    showConfirmButton: false,
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                    html: `<center><table class="table table-bordered text-center"><thead><tr><th>`+resp.index[0]+`</th><th>`+resp.index[1]+`</th><th>`+resp.index[2]+`</th></tr></thead><tbody><tr><td>`+((resp.values[0]/resp.length_df)*100).toFixed(2)+`%</td><td>`+((resp.values[1]/resp.length_df)*100).toFixed(2)+`%</td><td>`+((resp.values[2]/resp.length_df)*100).toFixed(2)+`%</td></tr></tbody></table></center><br/>`+`<a id="btn_download" href="/api/predict/file/download" class="btn btn-success" target="blank">Download File</a>`,
                });
            });
        }
    });

    $('#btn_upload_dataset').on('click', () => {
        if($('#form_upload_dataset')[0].files.length === 0){
            Swal.fire({
                title: 'File Not Found',
                icon: 'error',
                showCloseButton: true,
                showConfirmButton: false,
                allowEscapeKey: false,
                allowOutsideClick: false,
            });
        } else {
            form_data = new FormData($('#upload_file_dataset')[0]);
            $.ajax({
                url: '/api/file/merge',
                type: 'POST',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
            }).done( (resp) => {
                Swal.fire({
                    title: resp.result,
                    icon: 'success',
                    showConfirmButton: false,
                    showCloseButton: true,
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                });
            });
        }
    });

    $('#btn_upload_emoji').on('click', () => {
        if($('#form_upload_emoji')[0].files.length === 0){
            Swal.fire({
                title: 'File Not Found',
                icon: 'error',
                showCloseButton: true,
                showConfirmButton: false,
                allowEscapeKey: false,
                allowOutsideClick: false,
            });
        } else {
            form_data = new FormData($('#upload_file_emoji')[0]);
            $.ajax({
                url: '/api/file/emoji',
                type: 'POST',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
            }).done( (resp) => {
                Swal.fire({
                    title: resp.result,
                    icon: 'success',
                    showConfirmButton: false,
                    showCloseButton: true,
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                });
            });
        }
    });

    $('#btn_upload_emoticon').on('click', () => {
        if($('#form_upload_emoticon')[0].files.length === 0){
            Swal.fire({
                title: 'File Not Found',
                icon: 'error',
                showCloseButton: true,
                showConfirmButton: false,
                allowEscapeKey: false,
                allowOutsideClick: false,
            });
        } else {
            form_data = new FormData($('#upload_file_emoticon')[0]);
            $.ajax({
                url: '/api/file/emoticon',
                type: 'POST',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
            }).done( (resp) => {
                Swal.fire({
                    title: resp.result,
                    icon: 'success',
                    showConfirmButton: false,
                    showCloseButton: true,
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                });
            });
        }
    });

    $('#btn_reset_dataset').on('click', () => {
        $.ajax({
            url: '/api/file/merge',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                'command' : 'reset'
            }),
            success: (resp) => {
                Swal.fire({
                    title: resp.result,
                    icon: 'success',
                    showConfirmButton: false,
                    showCloseButton: true,
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                });
            }
        });
    });

    $('#btn_upload_stopwords').on('click', () => {
        if($('#form_upload_stopwords')[0].files.length === 0){
            Swal.fire({
                title: 'File Not Found',
                icon: 'error',
                showCloseButton: true,
                showConfirmButton: false,
                allowEscapeKey: false,
                allowOutsideClick: false,
            });
        } else {
            form_data = new FormData($('#upload_file_stopwords')[0]);
            $.ajax({
                url: '/api/file/stopwords',
                type: 'POST',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
            }).done( (resp) => {
                Swal.fire({
                    title: resp.result,
                    icon: 'success',
                    showConfirmButton: false,
                    showCloseButton: true,
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                });
            });
        }
    });

    $('#btn_upload_normalization').on('click', () => {
        if($('#form_upload_normalization')[0].files.length === 0){
            Swal.fire({
                title: 'File Not Found',
                icon: 'error',
                showCloseButton: true,
                showConfirmButton: false,
                allowEscapeKey: false,
                allowOutsideClick: false,
            });
        } else {
            form_data = new FormData($('#upload_file_normalization')[0]);
            $.ajax({
                url: '/api/file/normalization',
                type: 'POST',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
            }).done( (resp) => {
                Swal.fire({
                    title: resp.result,
                    icon: 'success',
                    showConfirmButton: false,
                    showCloseButton: true,
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                });
            });
        }
    });

    $('#btn_train').on('click', () => {
        Swal.fire({
            title: 'Are you sure?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
            allowEscapeKey: false,
            allowOutsideClick: false,
            reverseButtons: true,
        }).then( (result) => {
            if(result.isConfirmed){
                Swal.fire({
                    title: 'Training',
                    icon: 'info',
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                    onOpen: () => {
                        swal.showLoading();
                    }
                });
                $.ajax({
                    url: '/api/model/train',
                    type: 'POST',
                    contentType: false,
                    cache: false,
                    processData: false,
                    beforeSend: () => {
                        $('#btn_train').prop('disabled', true);
                        $('#btn_file_predict').prop('disabled', true);
                        $('#btn_text_predict').prop('disabled', true);
                        $('#btn_train span').text("Train...");
                    },
                }).done( (resp) => {             
                    Swal.close();
                    Swal.fire({
                        title: 'Training Success',
                        text: `Training Time : ` + resp.training_time + ` minutes`,
                        icon: 'success',
                        allowEscapeKey: false,
                        allowOutsideClick: false,
                        showCloseButton: false,
                    });
                    $('#btn_train span').text("Success");
                    setTimeout( () => {
                        $('#btn_train').prop('disabled', false);
                        $('#btn_file_predict').prop('disabled', false);
                        $('#btn_text_predict').prop('disabled', false);
                    }, 3000);
                    setTimeout( () => {
                        $('#btn_train span').text("Train");
                    }, 3000);
                    getModelInfo();
                });
            } else if (result.dismiss == Swal.DismissReason.cancel){
                Swal.fire({
                    title: 'Train Dataset has Cancel',
                    icon: 'error',
                    showConfirmButton: false,
                    showCloseButton: true,
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                });
            }
        });
    });

    $('#reloadData').on('click', () => {
        $('#body_cfm tr').remove();
        getModelInfo();
        getConfusionMatrix();
    });

    getConfusionMatrix();
    getModelInfo();
});