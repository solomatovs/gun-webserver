import sys, time

user_id = sys.argv[1]
count = 0

while True:
    count += 1
    print(f"[{user_id}] Tick {count}")
    time.sleep(1)
