class TuringMachine:
    def __init__(self, initial_state='Q0', final_state=None):
        self.tape = ['B']
        self.head_position = 0
        self.state = initial_state
        self.final_state = final_state
        
    def write_input(self, input_str):
        self.tape = list(input_str) + ['B']
        self.head_position = 0
        
    def move(self, direction):
        if direction == 'R':
            self.head_position += 1
            if self.head_position == len(self.tape):
                self.tape.append('B')
        elif direction == 'L':
            self.head_position = max(0, self.head_position - 1)
            
    def read(self):
        return self.tape[self.head_position]
    
    def write(self, symbol):
        self.tape[self.head_position] = symbol
        
    def run(self, transitions):
        while True:
            current_char = self.read()
            print(self.tape, self.head_position, self.state, current_char)
            if (self.state, current_char) not in transitions or self.state == self.final_state:
                break
                
            new_state, new_char, direction = transitions[(self.state, current_char)]
            self.write(new_char)
            self.move(direction)
            self.state = new_state
        return self.state == self.final_state
        
            
    def get_tape(self):
        return ''.join(self.tape).rstrip('B')

# Contoh penggunaan untuk mengganti semua '0' menjadi '1'
if __name__ == "__main__":
    # Membuat mesin Turing
    tm = TuringMachine(final_state='Q3')

    # Mendefinisikan transisi
    # Format: (state_sekarang, simbol_dibaca): (state_baru, simbol_tulis, arah)
    transitions = {
        ('Q0', '1'): ('Q0', '1', 'R'),
        ('Q0', '+'): ('Q1', '1', 'R'), # Jika ada simbol '+', timpa dengan '1'
        ('Q1', '1'): ('Q1', '1', 'R'),
        ('Q1', 'B'): ('Q2', 'B', 'L'),
        ('Q2', '1'): ('Q3', 'B', 'R') # Simbol '1' paling akhir dihapus
    }
    # Menjalankan mesin dengan input
    input_str = "111+11"
    tm.write_input(input_str)
    print(f"Input: {input_str}")
    tm.run(transitions)
    print(f"Output: {tm.get_tape()}")

    tm = TuringMachine(final_state='Q6')
    transitions = {
        # Q0: Tetap di Q0 jika simbol '1', pindah ke Q1 jika simbol '-'
        ('Q0', '1'): ('Q0', '1', 'R'),  # Tetap '1', gerak kanan
        ('Q0', '-'): ('Q1', '-', 'R'),  # Tetap '-', gerak kanan

        # Q1: Tetap di Q1 untuk '1', pindah ke Q2 jika simbol kosong ('B')
        ('Q1', '1'): ('Q1', '1', 'R'),  # Tetap '1', gerak kanan
        ('Q1', 'B'): ('Q2', 'B', 'L'),  # Tetap 'B', gerak kiri

        # Q2: Tandai simbol dan gerak ke kiri
        ('Q2', '1'): ('Q3', 'B', 'L'),  # Tandai '1' dengan 'B', gerak kiri
        ('Q2', '-'): ('Q6', 'B', 'L'),
    
        # Q3: Bergerak ke kiri, kembali ke Q2 jika menemukan '1' atau '-'
        ('Q3', '1'): ('Q3', '1', 'L'),  # Tetap '1', gerak kiri
        ('Q3', '-'): ('Q4', '-', 'L'),  # Tetap '-', gerak kiri

        # Q4: Bergerak ke kiri, kembali ke Q5 jika simbol kosong
        ('Q4', 'B'): ('Q4', 'B', 'L'),  # Tetap '1', gerak kiri
        ('Q4', '1'): ('Q5', 'B', 'R'),  # Kosong, gerak kanan ke Q5

        # Q5: Bergerak ke kanan untuk menyelesaikan
        ('Q5', 'B'): ('Q5', 'B', 'R'),  # Kosong, terima (akhir)
        ('Q5', '-'): ('Q1', '-', 'R'),  # Tetap '-', gerak kanan

        # Q6: Keadaan Akhir
        ('Q6', 'B'): ('Q6', 'B', 'R'),  # Tetap di Q6, terima
    }
    input_str = "1111-11"
    tm.write_input(input_str)
    print(f"Input: {input_str}")
    tm.run(transitions)
    print(f"Output: {tm.get_tape()}")

    tm = TuringMachine(final_state='Q7')
    transitions = {
        # Q0: Tandai simbol pertama dan gerak ke kanan
        ('Q0', 'a'): ('Q1', 'B', 'R'),  # Tetap 'a' dan gerak kanan
        ('Q0', 'b'): ('Q4', 'B', 'R'),  # Tetap 'b' dan gerak kanan
        ('Q0', 'B'): ('Q7', 'B', 'R'),  # Kosong, terima (akhir)

        # Q1: Lewati semua simbol di kanan hingga menemukan 'B'
        ('Q1', 'a'): ('Q1', 'a', 'R'),  # Lewati 'a'
        ('Q1', 'b'): ('Q1', 'b', 'R'),  # Lewati 'b'
        ('Q1', 'B'): ('Q2', 'B', 'L'),  # Kosong, gerak kiri

        # Q2: Periksa simbol terakhir dan kembali ke awal
        ('Q2', 'a'): ('Q3', 'B', 'L'),  # Tandai simbol 'a' terakhir

        # Q3: Bergerak ke kiri sampai kembali ke awal
        ('Q3', 'a'): ('Q3', 'a', 'L'),  # Lewati 'a'
        ('Q3', 'b'): ('Q3', 'b', 'L'),  # Lewati 'b'
        ('Q3', 'B'): ('Q0', 'B', 'R'),  # Kosong, kembali ke awal

        # Q4: Lewati semua simbol di kanan hingga menemukan 'B'
        ('Q4', 'a'): ('Q4', 'a', 'R'),  # Lewati 'a'
        ('Q4', 'b'): ('Q4', 'b', 'R'),  # Lewati 'b'
        ('Q4', 'B'): ('Q5', 'B', 'L'),  # Kosong, gerak kiri

        # Q5: Periksa simbol terakhir dan kembali ke awal
        ('Q5', 'b'): ('Q6', 'B', 'L'),  # Tandai simbol 'b' terakhir

        # Q6: Bergerak ke kiri sampai kembali ke awal
        ('Q6', 'a'): ('Q6', 'a', 'L'),  # Lewati 'a'
        ('Q6', 'b'): ('Q6', 'b', 'L'),  # Lewati 'b'
        ('Q6', 'B'): ('Q0', 'B', 'R'),  # Kosong, kembali ke awal

        # Q7: Keadaan Akhir
        ('Q7', 'B'): ('Q7', 'B', 'R'),  # Tetap di Q7, terima
    }
    input_str = "abaaba"
    tm.write_input(input_str)
    print(f"Input: {input_str}")
    res = tm.run(transitions)
    print(f"Output: {"Ya" if res else "Tidak"}")