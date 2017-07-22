#!/usr/bin/env python
'''
  generate a dotplot of a fasta against itself, or two fastas
  Usage:
    python dotplot.py < source.fa
'''

import argparse
import collections
import logging
from PIL import Image
import sys

COMPLEMENT = { 'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C', 'N': 'N' }
MAX_WIDTH=2048

def reverse_complement(s):
  '''
    return the reverse complement of the input string
  '''
  return ''.join(reversed([ COMPLEMENT[x] for x in s]))

def dotplot(k, genome, start, finish, output):
  '''
    generate a dotplot image of the stdin vs the genome
  '''
  genome1 = ''
  logging.info("reading fasta from stdin...")
  for line in sys.stdin:
    if line.startswith('>'):
      continue
    genome1 += line.strip()

  logging.info("reading fasta from stdin: read %i bases", len(genome1))
  if genome is None:
    genome2 = genome1
    logging.debug("dotplot will performed against itself")
  else:
    logging.info("reading %s...", genome)
    genome2 = ''
    for line in open(genome, 'r'):
      if line.startswith('>'):
        continue
      genome2 += line.strip()
    logging.info("reading fasta from %s: read %i bases", genome, len(genome2))
    
  genome_end = min(len(genome1), len(genome2), finish)

  logging.info("done reading fasta files. k is %i. showing range %i to %i.", k, start, genome_end)

  if genome_end - start > MAX_WIDTH:
    logging.error("image size too large: %i > %i", genome_end - start, MAX_WIDTH)
    return

  kmers1 = collections.defaultdict(set)
  kmers2 = collections.defaultdict(set)
  for pos in range(start, genome_end - k + 1):
    kmer = genome1[pos:pos+k].upper()
    kmers1[kmer].add(pos)
    rckmer = reverse_complement(kmer)
    kmers1[rckmer].add(pos + k - 1)

    kmer = genome2[pos:pos+k].upper()
    rckmer = reverse_complement(kmer)
    kmers2[kmer].add(pos)
    kmers2[rckmer].add(pos + k - 1)
    
  logging.debug("creating image")
    
  image = Image.new( 'RGB', (genome_end - start, genome_end - start), "white" )
  pixels = image.load()

  for kmer1 in kmers1:
    for kmer2_pos in kmers2[kmer1]:
      for kmer1_pos in kmers1[kmer1]:
        pixels[kmer1_pos - start, kmer2_pos - start] = (0, 0, 0)
        pixels[kmer2_pos - start, kmer1_pos - start] = (0, 0, 0)
      
  if output is None:
    logging.debug("showing image")
    image.show()
  else:
    logging.debug("saving image")
    image.save(output)
  logging.info("done")

def main():
  parser = argparse.ArgumentParser(description='Dotplots')
  parser.add_argument('--k', type=int, default=5, help='k')
  parser.add_argument('--genome', help='additional genome')
  parser.add_argument('--start', type=int, default=0, help='additional genome')
  parser.add_argument('--finish', type=int, default=1e9, help='additional genome')
  parser.add_argument('--output', help='output file to save image to')
  parser.add_argument('--verbose', required=False, action='store_true')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
  dotplot(args.k, args.genome, args.start, args.finish, args.output)

if __name__ == '__main__':
  main()
