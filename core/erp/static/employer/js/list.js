$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
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
            {"data": "names"},
            {"data": "dni"},
            {"data": "image"},
            {"data": "email"},
            {"data": "position.name_position"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                }
            },
            // {
            //     targets: [-3],
            //     class: 'text-center',
            //     orderable: false,
            //     render: function (data, type, row) {
            //         if(row.stock > 0){
            //             return '<span class="badge badge-success">'+data+'</span>'
            //         }
            //         return '<span class="badge badge-danger">'+data+'</span>'
            //     }
            // },
            // {
            //     targets: [-2],
            //     class: 'text-center',
            //     orderable: false,
            //     render: function (data, type, row) {
            //         return '$'+parseFloat(data).toFixed(2);
            //     }
            // },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/employer/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';                    
                    buttons += '<a href="/erp/employer/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';                    
                    // buttons += '<a href="/erp/employer/delete/' + row.id + '/" type="button" class="btn btn-success btn-xs btn-flat"><i class="fas fa-chart-pie"></i></a> ';
                    buttons += '<a href="/erp/employer/invoice/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    
                    
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});
