"""
When data is larger than RAM, systems use optimized storage techniques so the algorithm still “feels” fast even though most data lives on disk/SSD.

Core idea:
• Keep only the most useful data in RAM
• Store the full dataset on SSD/disk
• Read/write in chunks instead of loading everything
• Use indexing + caching so searches remain fast

Simple real-world example:
Imagine searching 1 billion user records.

Without optimization:
• Load everything into RAM
• Impossible if RAM is only 16GB

With optimized storage:
• Store records on SSD
• Keep only:
• index
• recent searches
• cache
in RAM

Search becomes:

Use RAM index → quickly find location
Fetch only required block from SSD
Return result

This is how databases like Google, MongoDB, and Redis scale.

Example Algorithm: External Merge Sort

Problem:
Sort a 50GB file using only 2GB RAM.

Approach:

Read small chunks
Sort each chunk in memory
Save sorted chunks to disk
Merge chunks efficiently

Complexity:
• RAM usage → fixed
• Can process unlimited file size

Algorithm:

Divide file into chunks
Sort each chunk
Store temporary sorted files
Merge using min-heap
"""
import heapq
import os

CHUNK_SIZE = 1000

def create_chunks(input_file):
    chunks = []

    with open(input_file, 'r') as f:
        chunk = []
        chunk_id = 0

        for line in f:
            chunk.append(int(line.strip()))

            if len(chunk) >= CHUNK_SIZE:
                chunk.sort()

                chunk_file = f'chunk_{chunk_id}.txt'

                with open(chunk_file, 'w') as cf:
                    for num in chunk:
                        cf.write(f"{num}\n")

                chunks.append(chunk_file)
                chunk = []
                chunk_id += 1

        if chunk:
            chunk.sort()

            chunk_file = f'chunk_{chunk_id}.txt'

            with open(chunk_file, 'w') as cf:
                for num in chunk:
                    cf.write(f"{num}\n")

            chunks.append(chunk_file)

    return chunks


def merge_chunks(chunks, output_file):
    files = [open(chunk, 'r') for chunk in chunks]

    heap = []

    for i, f in enumerate(files):
        num = f.readline().strip()
        if num:
            heapq.heappush(heap, (int(num), i))

    with open(output_file, 'w') as out:
        while heap:
            smallest, file_index = heapq.heappop(heap)

            out.write(f"{smallest}\n")

            next_num = files[file_index].readline().strip()

            if next_num:
                heapq.heappush(heap, (int(next_num), file_index))

    for f in files:
        f.close()

    for chunk in chunks:
        os.remove(chunk)


# Example usage
chunks = create_chunks('big_input.txt')
merge_chunks(chunks, 'sorted_output.txt')

print("Sorting completed!")