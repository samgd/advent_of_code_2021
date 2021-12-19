"""

Packet bits:
    3-5: version
    0-2: type ID

type ID 4 packets represent a "literal value", encoding a single 
binary number. Value padded with zeros until length is multiple 
of 4, then broken into groups of 4. Each group prefixed with 1
except last group, which is prefixed with a 0. 

other types IDs represent an "operator" that performs a 
calculation on one or more subpackets contained within. An
operator packet contains one or more packets. An operator packet 
contains one or more packets. To indicate which subsequent binary 
data represents its sub-packets, an operator packet can use one 
of two modes indicated by the bit immediately after the packet 
head; called the "length type ID".

    - 0: the next 15 bits are a number that represents the total
         length in bits of the sub-packets
    - 1: the next 11 bits are a number that represents the number 
         of sub-packets immediately contained by this packet

after the length type ID bit and the 15-bit or 11-bit field the 
subpackets appear
"""
import argparse
import operator
from dataclasses import dataclass
from functools import reduce
from typing import List

import bitstring
from bitstring import BitArray
from bitstring import ConstBitStream


@dataclass
class Packet:
    version: int
    type_id: int


@dataclass
class Literal(Packet):
    type_id = 4
    value: int
    
    def __init__(self, version: int, value: int):
        self.version = version
        self.value = value

    @staticmethod
    def from_bits(bits: ConstBitStream) -> "Literal":
        """Returns a Literal parsed from bits.

        Example:

            >>> s = ConstBitStream('0b110100101111111000101000')
            >>> Literal.from_bits(s)
            Literal(version=6, type_id=4, value=2021)
        """
        version = bits.read("uint:3")
        type_id = bits.read("uint:3")
        if type_id != Literal.type_id:
            raise ValueError(f"Literal type ID={Literal.type_id}, found {type_id}")
        value = 0
        more_groups = True
        while more_groups:
            more_groups = bits.read("bool")
            value = (value << 4) + bits.read("uint:4")
        return Literal(version, value)


@dataclass
class Operator(Packet):
    
    sub_packets: List[Packet]
    
    def __init__(self, version: int, type_id: int, sub_packets: List[Packet]):
        self.version = version
        self.type_id = type_id
        self.sub_packets = sub_packets

    @staticmethod
    def from_bits(bits: ConstBitStream) -> "Operator":
        """Returns an Operator parsed from bits.

        Example:
        
            >>> s = ConstBitStream('0b00111000000000000110111101000101001010010001001000000000')
            >>> print(Operator.from_bits(s))
            Operator(version=1, type_id=6, sub_packets=[Literal(version=6, type_id=4, value=10), Literal(version=2, type_id=4, value=20)])
        """
        version = bits.read("uint:3")
        type_id = bits.read("uint:3")
        if type_id == Literal.type_id:
            raise ValueError(f"Operator type ID!={Literal.type_id}")
        length_type_id = bits.read("bool")
        if length_type_id == 0:
            n_subpackets = float("inf")
            subpacket_bits = bits.read("uint:15")
        else:
            n_subpackets = bits.read("uint:11")
            subpacket_bits = float("inf")
        n_parsed = 0
        start = bits.bitpos
        subpackets = []
        while n_parsed < n_subpackets and (bits.bitpos - start) < subpacket_bits:
            _, next_type_id = bits.peeklist(["uint:3", "uint:3"])
            if next_type_id == 4:
                subpackets.append(Literal.from_bits(bits))
            else:
                subpackets.append(Operator.from_bits(bits))
            n_parsed += 1
        return Operator(version, type_id, subpackets)


def from_bits(bits: ConstBitStream) -> Packet:
    _, type_id = bits.peeklist(["uint:3", "uint:3"])
    if type_id == 4:
        return Literal.from_bits(bits)
    return Operator.from_bits(bits)


def version_sum(packet: Packet) -> int:
    if isinstance(packet, Literal):
        return packet.version
    return packet.version + sum([version_sum(p) for p in packet.sub_packets])


def calculate(packet: Packet) -> int:
    """Returns the value of the expression in packet.

    Example:

        >>> parse = lambda h: from_bits(ConstBitStream(hex=h))
        >>> calculate(parse("C200B40A82"))
        3
        >>> calculate(parse("04005AC33890"))
        54
        >>> calculate(parse("880086C3E88112"))
        7
        >>> calculate(parse("CE00C43D881120"))
        9
        >>> calculate(parse("D8005AC2A8F0"))
        1
        >>> calculate(parse("F600BC2D8F"))
        0
        >>> calculate(parse("9C005AC2F8F0"))
        0
        >>> calculate(parse("9C0141080250320F1802104A08"))
        1
    """
    if packet.type_id == 4: return packet.value
    sps = [calculate(sp) for sp in packet.sub_packets]
    if packet.type_id == 0: return sum(sps)
    if packet.type_id == 1: return reduce(operator.mul, sps, 1)
    if packet.type_id == 2: return min(sps)
    if packet.type_id == 3: return max(sps)
    if packet.type_id == 5: return int(sps[0] > sps[1])
    if packet.type_id == 6: return int(sps[0] < sps[1])
    if packet.type_id == 7: return int(sps[0] == sps[1])
    raise NotImplementedError(f"unknown {packet.type_id=}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--path", default=None)
    group.add_argument("--hex", default=None)
    args = parser.parse_args()

    if args.path is not None:
        with open(args.path, 'r') as f:
            bits = ConstBitStream(hex=f.readline().strip())
    elif args.hex is not None:
        bits = ConstBitStream(hex=args.hex)
        
    packets = from_bits(bits)
    print(version_sum(packets))

    print(calculate(packets))