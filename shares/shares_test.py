import threading
from shares.shares_real_time_prices import Stock


if __name__ == '__main__':
    share = Stock('sh600884,sz000008', 5)
    thread = threading.Thread(target=share.run)
    thread.start()
    while True:
        print(share.work_queue.get())
        share.work_queue.task_done()
