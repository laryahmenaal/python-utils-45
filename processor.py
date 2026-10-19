import hashlib
import multiprocessing as mp
from typing import List, Optional

class HashOptimizer:
    def __init__(self, cores: int = mp.cpu_count()):
        self.cores = cores

    def _chunk_process(self, data: List[bytes]) -> List[str]:
        results = []
        for item in data:
            hasher = hashlib.blake2b(digest_size=32)
            hasher.update(item)
            results.append(hasher.hexdigest())
        return results

    def batch_process(self, data: List[bytes]) -> List[str]:
        if len(data) < 1000:
            return self._chunk_process(data)
            
        chunk_size = len(data) // self.cores
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
        with mp.Pool(processes=self.cores) as pool:
            results = pool.map(self._chunk_process, chunks)
        
        return [item for sublist in results for item in sublist]

def run_optimization(payloads: List[bytes]) -> List[str]:
    optimizer = HashOptimizer()
    return optimizer.batch_process(payloads)