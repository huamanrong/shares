import threading


def create_thread(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()


if __name__ == '__main__':
    import time
    import inspect
    import ctypes


    def _async_raise(tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")


    def stop_thread(thread):
        _async_raise(thread.ident, SystemExit)


    def thread_test():
        while True:
            print('-------')
            time.sleep(0.5)


    # 添加线程的页面，把 页面: 线程id 传入字典，切面切换时就可以停止指定的线程
    t = threading.Thread(target=thread_test)
    t.start()
    time.sleep(5.2)
    print("main thread sleep finish")
    stop_thread(t)
