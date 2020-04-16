import CoreModules.path as path
import CoreModules.crawler as crawler
import config

from multiprocessing.dummy import Pool as ThreadPool

import sys
import os
import time

# measure execute time
start_time = time.time()

# clear console
os.system('cls||clear')

# option
first_run = input('Frist run? (Y as default) ')
if first_run.lower() != 'n':
    path.remove(config.RESULT_FILE)
    path.remove(config.BUG_FILE)

# run mode
test_mode = input('Test mode ? only run on 200 webs (Y as default) ')

# threads number
threads_run = input('How many threads ? (50 as default) ')
if not threads_run:
    number_threads = int(50)
else:
    number_threads = int(threads_run.strip())

time.sleep(1)
print("Exe with " + str(number_threads) + " threads...")
time.sleep(3)

def main():

    with open(config.SOURCE_FILE) as FileObj:

        list_rank = []
        list_url = []

        for index, item in enumerate(FileObj):

            rank = crawler.get_rank(item).strip()
            list_rank.append(rank)

            url = crawler.get_url(item).strip()
            list_url.append(url)

            # run mode
            if test_mode.lower() != 'n':
                if index > 200:
                    break

    pool = ThreadPool(number_threads)
    process = pool.starmap(crawler.get_info, zip(list_rank, list_url))

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()

    message = "-------- %s seconds --------" % (time.time() - start_time)
    print(message)
    
    with open(config.BUG_FILE, 'a', encoding="utf-8") as f:
        f.writelines("\n\n" + str(message))