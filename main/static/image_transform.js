window.onload = function () {
    let img = document.querySelector("#image")
    let form = document.querySelector("#transform_form")
    form.reset()    //reset data on reload

    form.onchange = function () {
        let transformation = ""
        let rotation = form.rotation.value

        if (rotation == "0")
            transformation += "rotate(0deg)"
        else if (rotation == "270")
            transformation += "rotate(270deg)"
        else if (rotation == "90")
            transformation += "rotate(90deg)"
        else if (rotation == "180")
            transformation += "rotate(180deg)"

        transformation += form.mirror_x.checked ? " scaleX(-1)" : " scaleX(1)"
        transformation += form.mirror_y.checked ? " scaleY(-1)" : " scaleY(1)"

        img.style.transform = transformation
    }


}