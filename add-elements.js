$(document).ready(
    function()
    {
        $("#button").click(

            function()
            {
                $.post("/element-add-handler.html",
                {
                    number: $("#element-number").val(),
                    code: $("#element-code").val(),
                    name: $("#element-name").val(),
                    color1: $("#element-color1").val(),
                    color2: $("#element-color2").val(),
                    color3: $("#element-color3").val(),
                    radius: $("#element-radius").val()
                }
                );
            }
        );
    }
);