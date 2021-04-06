var map, handler;
var zoom = 12;
var lay;
var onlyMapLay;


/**
 * 加载地图
 */
function onLoad() {
    var imageURL = "http://t0.tianditu.gov.cn/img_w/wmts?" +
        "SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles" +
        "&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=xxxxx";

    //创建自定义图层对象
    lay = new T.TileLayer(imageURL, {
        minZoom: 1,
        maxZoom: 18
    });
    var config = {
        layers: [lay]
    };

    //初始化地图对象
    map = new T.Map("mapDiv", config);
    map.centerAndZoom(new T.LngLat(113.40769, 22.20945), zoom);
    map.enableScrollWheelZoom();

    //创建标注工具对象
    polygonTool = new T.PolygonTool(map, config);
}


/**
 * 绘制矩形
 */
function openRectangleTool() {
    map.clearOverLays();
    if (handler) handler.close();
    handler = new T.RectangleTool(map, {
        follow: true
    });
    handler.open();
    handler.addEventListener("draw", onDrawRectangle);
}


/**
 * 矩形绘制完成，传递坐标
 */
function onDrawRectangle(e) {
    var tr_lat = e.currentBounds.Lq.lat;
    var tr_lng = e.currentBounds.Lq.lng;
    var bl_lat = e.currentBounds.kq.lat;
    var bl_lng = e.currentBounds.kq.lng;
    document.getElementById("tl_lng").value = bl_lng;
    document.getElementById("tl_lat").value = tr_lat;
    document.getElementById("br_lng").value = tr_lng;
    document.getElementById("br_lat").value = bl_lat;
}


function submitCoordForm() {
    var elements = document.getElementsByClassName("coord_input");
    var postData = (function (obj) {
        var str = "";
        for (var i = 0; i < obj.length; i++) {
            str += obj[i].name + "=" + obj[i].value + "&"
        }
        return str;
    })(elements);

    var xhr = new XMLHttpRequest();
    xhr.open("post", "/image");
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById("download_file_name").value = xhr.responseText;
            alert("卫片已生成！")
        }
    }
    xhr.send(postData);
}


function downloadImage(){
    var filename = document.getElementById("download_file_name").value;
    var xhr = new XMLHttpRequest();
    url = "/download/" + filename;
    xhr.open("get", url, true);
    xhr.responseType = "blob";
    xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var content = xhr.response;
            var file_url = window.URL.createObjectURL(new Blob([content]), {type: ' image/tiff'})
            var link = document.createElement("a");
            link.style.display = "none";
            link.href = file_url;
            link.download = xhr.getResponseHeader('filename');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
    xhr.send();
}