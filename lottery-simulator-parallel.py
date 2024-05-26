from collections import defaultdict
from multiprocessing import Pool, cpu_count
import numpy as np
import time

def generate_lottery_numbers():
    main_numbers = tuple(sorted(np.random.choice(range(1, 50), 5, replace=False)))
    lucky_number = np.random.randint(1, 11)
    return main_numbers + (lucky_number,)

def simulate_lottery_draws_chunk(chunk_size):
    draw_counts = defaultdict(int)
    for _ in range(chunk_size):
        draw = generate_lottery_numbers()
        draw_counts[draw] += 1
    return draw_counts

def merge_counts(counts_list):
    merged_counts = defaultdict(int)
    for counts in counts_list:
        for draw, count in counts.items():
            merged_counts[draw] += count
    return merged_counts

def simulate_lottery_draws_parallel(num_draws, max_workers=4):
    num_workers = min(max_workers, cpu_count())
    chunk_size = num_draws // num_workers
    remainder = num_draws % num_workers

    chunks = [chunk_size] * num_workers
    for i in range(remainder):
        chunks[i] += 1

    start_time = time.time()

    with Pool(num_workers) as pool:
        counts_list = pool.map(simulate_lottery_draws_chunk, chunks)
    
    merged_counts = merge_counts(counts_list)
    total_time = time.time() - start_time

    return merged_counts, total_time

def find_most_frequent_draw(draw_counts):
    most_frequent_draw = max(draw_counts, key=draw_counts.get)
    return most_frequent_draw, draw_counts[most_frequent_draw]

if __name__ == '__main__':
    num_draws = 12000000
    results, elapsed_time = simulate_lottery_draws_parallel(num_draws, max_workers=cpu_count())

    most_frequent_draw, max_count = find_most_frequent_draw(results)
    print(f"La grille la plus fréquente est {most_frequent_draw} avec {max_count} occurrences.")
    print(f"Le temps total d'exécution est de {elapsed_time:.2f} secondes.")
