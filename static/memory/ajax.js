window.addEventListener("load" , function (){

    $(document).on("click", "#submit", function(){ submit(); });

    $(document).on("input", ".image_input", function(){

        //最後のinput要素にinputされた時、新しいinputを追加する。これを次の兄弟要素を抜き取る.next()と.lengthで判定する。(0なら最後の要素)
        if ( !$(this).next().length ){
            $("#image_input_area").append('<input class="image_input" type="file" name="image">');
        }
    })
});

function submit(){

    let form_elem   = "#form_area";

    let data    = new FormData( $(form_elem).get(0) );
    let url     = $(form_elem).prop("action");
    let method  = $(form_elem).prop("method");

    for (let v of data ){ console.log(v); }

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 

        if (data.error){
            console.log("ERROR");
        }
        else{
            $("#content_area").html(data.content);
            $("#textarea").val("");
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 

}