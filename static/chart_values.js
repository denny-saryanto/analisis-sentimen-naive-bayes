$(document).ready( () => {

    let color = ['#7ec2e7', '#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de', '#f64f2c', '#117ea6', '#82e4de'];

    reqBarData = () => {
        $.ajax({
            url: '/api/count/labels',
            type: 'POST',
            dataType: 'JSON',
            success: (data) => {
                getTop10Words(data.index, data.values, '#pieChart');
                $('#panjangDF').text(data.length_df);
            },
        });
    }

    reqPieData = () => {
        $.ajax({
            url: '/api/count/words',
            type: 'POST',
            dataType: 'JSON',
            success: (data) => {
                chartFunc(data.index, data.values);
                getWordsLabel(data.positive_words.value, data.positive_words.label, '#positiveWordChart');
                getWordsLabel(data.neutral_words.value, data.neutral_words.label, '#neutralWordChart');
                getWordsLabel(data.negative_words.value, data.negative_words.label, '#negativeWordChart');
                console.log(data.positive_words);
            },
        });
    }

    getWordsLabel = (value, label, id) => {
        let chart = new Chart($(id)[0].getContext('2d'), {
            type: 'horizontalBar',
            data: {
                labels: label,
                datasets: [{
                    data: value,
                    backgroundColor : color,
                }]
            },
            options: {
                legend: { 
                    display: false 
                },
                maintainAspectRatio : false,
                responsive : true,
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

    getAllWords = () => {
        $.ajax({
            url: '/api/info',
            type: 'GET',
            dataType: 'JSON',
            success: (resp) => {
                $('#allWords').text(resp.all_words);
                $('#getStopwords').text(resp.total_stopwords);
                $('#normalizationData').text(resp.total_normalization);
            }
        });
    }

    chartFunc = (label, value) => {
        let myBarChart = new Chart($('#stackedBarChart')[0].getContext('2d'), {
            type: 'bar',
            data: {
                labels: label,
                datasets: [{
                    data: value,
                    backgroundColor : color,
                }]
            },
            options: {
                legend: { 
                    display: false 
                },
                maintainAspectRatio : false,
                responsive : true,
            }
        });
    }

    $('#reloadData').click( () => {
        reqBarData();
        reqPieData();
        getAllWords();
    });

    getAllWords();
    reqBarData();
    reqPieData();
});