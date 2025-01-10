from collections import defaultdict

class Node:
    def __init__(self, value, character=None):
        self.value = value
        self.character = character
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.value < other.value

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, node):
        self.heap.append(node)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if len(self.heap) > 1:
            self._swap(0, len(self.heap) - 1)
            min_node = self.heap.pop()
            self._heapify_down(0)
        else:
            min_node = self.heap.pop()
        return min_node

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index].value < self.heap[parent].value:
            self._swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.heap) and self.heap[left].value < self.heap[smallest].value:
            smallest = left
        if right < len(self.heap) and self.heap[right].value < self.heap[smallest].value:
            smallest = right
        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def __len__(self):
        return len(self.heap)

def count_characters(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    frequencies = defaultdict(int)
    for char in text:
        frequencies[char] += 1
    return frequencies, text

def build_huffman_tree(frequencies):
    queue = PriorityQueue()
    for char, freq in frequencies.items():
        queue.push(Node(freq, char))

    while len(queue) > 1:
        left = queue.pop()
        right = queue.pop()
        parent = Node(left.value + right.value)
        parent.left = left
        parent.right = right
        queue.push(parent)

    return queue.pop()

def generate_codes(node, code="", codes=None):
    if codes is None:
        codes = {}
    if node.character is not None:
        codes[node.character] = code
    else:
        if node.left:
            generate_codes(node.left, code + "0", codes)
        if node.right:
            generate_codes(node.right, code + "1", codes)
    return codes

def encode_text(text, codes):
    return "".join(codes[char] for char in text)

def save_encoded_file(encoded_text, codes, file_path):
    with open(file_path, "wb") as file:
        file.write((str(codes) + "\n").encode("utf-8"))
        padding = (8 - len(encoded_text) % 8) % 8
        encoded_text += "0" * padding
        file.write(int(encoded_text, 2).to_bytes((len(encoded_text) + 7) // 8, byteorder="big"))
        file.write(bytes([padding]))

def decode_file(file_path, output_path):
    with open(file_path, "rb") as file:
        codes_line = file.readline().decode("utf-8").strip()
        codes = eval(codes_line)
        reversed_codes = {v: k for k, v in codes.items()}
        data = file.read()
        padding = data[-1]
        binary = bin(int.from_bytes(data[:-1], byteorder="big"))[2:].zfill((len(data) - 1) * 8)
        binary = binary[:-padding]

    decoded_text = ""
    temp = ""
    for bit in binary:
        temp += bit
        if temp in reversed_codes:
            decoded_text += reversed_codes[temp]
            temp = ""

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(decoded_text)

def main():
    input_file = "input.txt"
    encoded_file = "encoded.bin"
    decoded_file = "decoded.txt"
    frequencies, text = count_characters(input_file)
    root = build_huffman_tree(frequencies)
    codes = generate_codes(root)
    encoded_text = encode_text(text, codes)
    save_encoded_file(encoded_text, codes, encoded_file)
    decode_file(encoded_file, decoded_file)

if __name__ == "__main__":
    main()
