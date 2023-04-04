$.ajax({
    url: "add-elements-to-table.html",
    type: "GET",
    dataType: "json",
    success: function(result){
        console.log("Hey there !!");

        var element = ''

        $.each(result, function(key, value){
            element += '<tr>';
            element += '<td>' + value.number + '</td>';
            element += '<td>' + value.code + '</td>';
            element += '<td>' + value.name + '</td>';
            element += '<td>' + value.color1 + '</td>';
            element += '<td>' + value.color2 + '</td>';
            element += '<td>' + value.color3 + '</td>';
            element += '<td>' + value.radius + '</td>';
            element += '<td><button id="button">Delete</button>'
            element += '</tr>'
        }
        );

        $('#table').append(element)
    },
    fail: function(result){
        console.log("lol cringe");
    }
});