import sys

class EnigmaMachine:
    def __init__(self, rotor_order=[0, 1, 2], reflector='B', plugboard_connections={}):
        self.rotors = [
            "EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # Rotor I
            "AJDKSIRUXBLHWTMCQGZNPYFVOE",  # Rotor II
            "BDFHJLCPRTXVZNYEIWGAKMUSQO"   # Rotor III
        ]
        self.reflector = {
            'B': "YRUHQSLDPXNGOKMIEBFZCWVJAT",
            'C': "FVPJIAOYEDRZXWGCTKUQSBNMHL"
        }[reflector]
        self.rotor_order = rotor_order
        self.rotor_positions = [0, 0, 0]
        self.plugboard = plugboard_connections

    def rotate_rotors(self):
        self.rotor_positions[0] = (self.rotor_positions[0] + 1) % 26
        if self.rotor_positions[0] == 0:
            self.rotor_positions[1] = (self.rotor_positions[1] + 1) % 26
            if self.rotor_positions[1] == 0:
                self.rotor_positions[2] = (self.rotor_positions[2] + 1) % 26

    def plugboard_swap(self, char):
        return self.plugboard.get(char, char)

    def forward_substitute(self, char, rotor, position):
        index = (ord(char) - ord('A') + position) % 26
        return rotor[index]

    def backward_substitute(self, char, rotor, position):
        index = (rotor.index(char) - position) % 26
        return chr(index + ord('A'))

    def substitute(self, char):
        char = self.plugboard_swap(char)
        for i in range(len(self.rotor_order)):
            rotor_index = self.rotor_order[i]
            position = self.rotor_positions[rotor_index]
            char = self.forward_substitute(char, self.rotors[rotor_index], position)
        char = self.reflector[(ord(char) - ord('A')) % 26]
        for i in range(len(self.rotor_order) - 1, -1, -1):
            rotor_index = self.rotor_order[i]
            position = self.rotor_positions[rotor_index]
            char = self.backward_substitute(char, self.rotors[rotor_index], position)
        return self.plugboard_swap(char)

    def process_message(self, message):
        processed_message = ''
        for char in message:
            if char.isalpha():
                self.rotate_rotors()
                processed_char = self.substitute(char.upper())
                processed_message += processed_char
        return processed_message

    def set_rotor_positions(self, positions):
        if len(positions) == 3:
            self.rotor_positions = positions
        else:
            print("Please provide positions for all three rotors.")

def get_plugboard_connections(input_str):
    connections = {}
    pairs = input_str.split()
    for pair in pairs:
        if len(pair) == 2:
            connections[pair[0].upper()] = pair[1].upper()
            connections[pair[1].upper()] = pair[0].upper()
    return connections

def main():
    if len(sys.argv) < 5:
        print("Usage: python enigma.py <rotor_positions> <reflector> <plugboard_connections> <message>")
        print("Example: python enigma.py 1 2 3 B 'A B C D' 'HELLO WORLD'")
        return

    rotor_positions = [int(pos) for pos in sys.argv[1:4]]
    reflector = sys.argv[4].upper()
    plugboard_connections = get_plugboard_connections(sys.argv[5])
    message = sys.argv[6]

    enigma = EnigmaMachine(reflector=reflector, plugboard_connections=plugboard_connections)
    enigma.set_rotor_positions(rotor_positions)

    encrypted_text = enigma.process_message(message)
    print("Encrypted:", encrypted_text)

    # Reset the rotor positions to the initial state for decryption
    enigma.set_rotor_positions(rotor_positions)

    decrypted_text = enigma.process_message(encrypted_text)
    print("Decrypted:", decrypted_text)

if __name__ == "__main__":
    main()





