import threading
import inspect
import ctypes


class ThreadUntil:
    thread_dict = {}

    @staticmethod
    def create_thread(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()
        return t

    @staticmethod
    def _async_raise(tid, exec_type):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exec_type):
            exec_type = type(exec_type)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exec_type))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        try:
            self._async_raise(thread.ident, SystemExit)
        except:
            pass


if __name__ == '__main__':
    # 添加线程的页面，把 页面: 线程id 传入字典，切面切换时就可以停止指定的线程
    pass
