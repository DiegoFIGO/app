$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: true,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: "",
            headers: {
                'X-CSRFToken': csrftoken
            }
        },
        columns: [
            {"data": "id"},
            // {"data": "name"},
            {"data": "personal.name"},
            // {"data": "organization"},
            {"data": "price"},
            // {"data": "offer"},
            // {"data": "request_personal"},
            // {"data": "request_material"},
            {"data": "observations"},
            // {"data": "date_registration"},
            // {"data": "date_start"},
            // {"data": "date_finish"},
            // {"data": "new"},
            // {"data": "finished"},
            // {"data": "process"},
            {"data": "id"},
            // {"data": "offer"},
        ],
        columnDefs: [
            // {
            //     // targets: [-1],
            //     targets: [-2],
            //     class: 'text-center',
            //     orderable: false,
            //     render: function (data, type, row) {
            //         return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
            //     }
            // },
            {
                targets: [-3],
                // class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$ '+parseFloat(data).toFixed(2);
                }
            },
            {
                // targets: [-2],
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/acquisitionb/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';                    
                    buttons += '<a href="/erp/acquisitionb/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';                    
                    // buttons += '<a href="/erp/project/details/' + row.id + '/" type="button" class="btn btn-success btn-xs btn-flat"><i class="fas fa-chart-pie"></i></a> ';
                    buttons += '<a href="/erp/acquisitionb/invoice/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    
                    
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
    
});
