import time


start_time = time.time()
# doing some simulation work
for i in range(100000):
    print(i)
end_time = time.time()
print(f"Time taken: {end_time - start_time}")

print("Waiting for 2 sec")
time.sleep(2)
print("Done")

local_time_struct = time.localtime(time.time())
print(f"Local time structure: {local_time_struct}")

current_gmt = time.gmtime()
print(f"Current GMT: {current_gmt}")
formatted_current_gmt = time.strftime("%Y-%m-%d %H:%M:%S", current_gmt)
print(f"Formatted current GMT: {formatted_current_gmt}")

