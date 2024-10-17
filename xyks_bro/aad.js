function create_fake_pthread_create() {
    const fake_pthread_create = Memory.alloc(4096)
    Memory.protect(fake_pthread_create, 4096, "rwx")
    Memory.patchCode(fake_pthread_create, 4096, code => {
        const cw = new Arm64Writer(code, {pc: ptr(fake_pthread_create)})
        cw.putRet()
    })
    return fake_pthread_create
}

function hook_dlsym() {
    let count = 0;
    sendLog("trace", "hook dlsym")
    const create = create_fake_pthread_create();
    const interceptor = Interceptor.attach(Module.findExportByName(null, "dlsym"),
        {
            onEnter: function (args) {
                const name = args[1].readCString()
                sendLog("trace", `[dlsym] ${name}`)
                if (name === "pthread_create")
                    count++
            },
            onLeave: function (retval) {
                if (count === 1) {
                    retval.replace(create)
                } else if (count === 2) {
                    retval.replace(create)
                    // 完成2次替换, 停止 hook dlsym
                    sendLog('trace', "unhook dlsym")
                    interceptor.detach()
                }
                sendLog("trace", "dlsym result faked")
            }
        }
    );
    return interceptor
}

function hook(soName = '') {
    sendLog("trace", "hook android_dlopen_ext")
    return Interceptor.attach(Module.findExportByName(null, "android_dlopen_ext"),
        {
            onEnter: function (args) {
                const path_ptr = args[0];
                if (path_ptr !== undefined && path_ptr != null) {
                    const path = path_ptr.readCString();
                    if (path.indexOf(soName) >= 0) {
                        sendLog("trace", `loading library ${path}`)
                        const interceptor = hook_dlsym();
                        // auto detach after 3 seconds
                        setTimeout(() => interceptor.detach(), 200)
                    }
                }
            }
        }
    )
}

function sendTyped(type, data) {
    send({
        type, data
    })
}

function sendLog(level, message) {
    sendTyped("log", {
        level,
        message
    })
}

setImmediate((library) => {
    const interceptor = hook(library)
    // auto detach after 3 seconds, probably user rm'd the so
    setTimeout(() => interceptor.detach(), 3000)
}, "libmsaoaidsec.so")