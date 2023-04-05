$(document).ready(
    function()
    {
        $("#button").click(

            function()
            {
                if ($("#element-number").val() > -1 && $("#element-number").val() != null && $("#element-code").val() != null && $("#element-code").val() != "" && $("#element-name").val() != null && $("#element-name").val() != "" && $("#element-radius").val() > 0 && $("#element-radius").val() != null){
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
                alert ("Successfully added.")
            }
            else{
                alert ("Something's not right. Please try again or check your inputs.")
            }
            }
        );
    }
);