const fix_media = () =>{
    media_server = `${location.protocol}//${location.hostname}:8080`
    document.querySelectorAll("img").forEach((img)=>{
        if(img.src.startsWith(`${window.origin}`)){
            fetch(img.src).then((res)=>{
                if(!res.ok){
                    let image = img.src.split("media/")[1]
                    img.src = `${media_server}/${image}`
                }
            })
        }
    })
}

fix_media();


const img_input = document.getElementById("id_image")
if(img_input != null){
    img_input.form.addEventListener("submit",(e)=>{
        let f = img_input.value.split(".")
        let img_types = ['png','jpeg','jpg','gif','webp','svg']
        img_input.labels[0].textContent += `(.${img_types.join(", .")})`
        let ext = f[f.length-1]
        if(ext != "" && !img_types.includes(ext.toLowerCase())){
            img_input.value = ""
            window.alert("Invalid image type. Form submited without image")
        }
    });
}