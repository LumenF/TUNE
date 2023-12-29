from django.utils.safestring import mark_safe


def preview_zoom(url):
    return mark_safe(
        f"""
            <div class="zoomer" onmousemove="zoom(event)" style="background-image: url({url});">
                <img src="{url}" />
            </div>
        """ +
        """

<style>
 .zoomer {
    background-position: 50% 50%;
    position: relative;
    width: 190px;
    height: 190px;
    overflow: hidden;
    cursor: zoom-in;
}
.zoomer img:hover {
    opacity: 0;
    width: 100%;
    height: 100%;
}
.zoomer img {
    transition: opacity 0s;
    width: 100%;
    height: 100%;
}
.zoomer:hover{
    width: 510px;
    height: 510px;
}
</style>
<script>
 function zoom(event) {
    let zoomer = event.currentTarget;
    event.offsetX ? (offsetX = event.offsetX) : (offsetX = event.touches[0].pageX);
    event.offsetY ? (offsetY = event.offsetY) : (offsetX = event.touches[0].pageX);
    let x = offsetX / zoomer.offsetWidth  * 100;
    let y = offsetY / zoomer.offsetHeight * 100;
    zoomer.style.backgroundPosition = x + "% " + y +"%";
}
</script>

        """
    )


def show_preview_display(url, width, height):
    return mark_safe(
            '<img'
            f' src="{url}"'
            f' width={width};'
            f' height={height};/>'
    )
