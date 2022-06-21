window.onload = function () {
    let vertical_image = document.querySelector("#vertical-image")
    let horizontal_image = document.querySelector("#horizontal-image")

    let vertical_container = document.querySelector("#vertical-image-container")
    let horizontal_container = document.querySelector("#horizontal-image-container")


    let form = document.querySelector("#transform_form")

    vertical_container.style.display = "none"
    horizontal_container.style.display = "block"

    form.reset()    //reset data on reload

    form.onchange = function () {
        let transformation = ""
        let rotation = form.rotation.value

        if (rotation == "0" || rotation == "180") {
            vertical_container.style.display = "none"
            horizontal_container.style.display = "block"
            
            if (rotation == "180")
                transformation += "rotate(180deg)"

            transformation += form.mirror_x.checked ? " scaleX(-1)" : " scaleX(1)"
            transformation += form.mirror_y.checked ? " scaleY(-1)" : " scaleY(1)"
            horizontal_image.style.transform = transformation
        }
        else if (rotation == "90" || rotation == "270") {
            //vertical img is rotated by 90 degrees clockwise, so rotating it opposite direction requires rotating it 180degree more
            vertical_container.style.display = "block"
            horizontal_container.style.display = "none"

            if (rotation == "270")
                transformation += "rotate(180deg)"

            transformation += form.mirror_x.checked ? " scaleX(-1)" : " scaleX(1)"
            transformation += form.mirror_y.checked ? " scaleY(-1)" : " scaleY(1)"
            vertical_image.style.transform = transformation
        }


    }


}