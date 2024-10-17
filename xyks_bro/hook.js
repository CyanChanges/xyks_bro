function hook() {
    Java.perform(() => {
        sendLog("trace", "perform hook")
        let r2 = Java.use("com.fenbi.android.leo.utils.r2");
        sendLog("trace", "r2 hook")
        r2.b.overload("[B").implementation = function (data) {
            let String = Java.use("java.lang.String");
            // sendLog("trace", "hooked encrypt method called")
            sendData(bytes2Hex(data))
            let patched
            recv("patch", (data) => {
                sendLog("trace", "received patched data")
                if (data.type !== 'patch')
                    throw new Error("bad response")
                patched = String.$new(data.data).getBytes();
            }).wait()
            return this["b"](patched);
        };

        sendLog("trace", "XYKS r2 method hooked")
        sendTyped('ready')
    });
}

function sendTyped(type, data) {
    send({
        type, data
    })
}

function sendData(data) {
    sendTyped('data', data)
}

function sendLog(level, message) {
    sendTyped("log", {
        level,
        message
    })
}

function bytes2Hex(arrBytes) {
    let str = "";
    for (var i = 0; i < arrBytes.length; i++) {
        let tmp;
        const num = arrBytes[i];
        if (num < 0) {
            //此处填坑，当byte因为符合位导致数值为负时候，需要对数据进行处理
            tmp = (255 + num + 1).toString(16);
        } else {
            tmp = num.toString(16);
        }
        if (tmp.length === 1) {
            tmp = "0" + tmp;
        }
        str += tmp;
    }
    return str;
}

setImmediate(hook);