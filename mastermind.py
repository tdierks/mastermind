#!/usr/bin/python

import argparse
import random
import sys

COLORS = 6
PINS = 4

def allPatterns():
  """Generator function to yield all possible color combinations"""
  cur = [0] * PINS
  while True:
    yield tuple(cur)
    for i in range(PINS):
      cur[i] += 1
      if cur[i] < COLORS:
        break
      cur[i] = 0
      if i == PINS - 1:
        return

def check(answer, probe):
  """Given an answer and a guess, return a score of (red, white)"""
  acolcnt = [0] * COLORS
  pcolcnt = [0] * COLORS
  
  red = 0
  for (a, p) in zip(answer, probe):
    if a == p:
      red = red + 1
    else:
      acolcnt[a] += 1
      pcolcnt[p] += 1
  white = 0
  for a, p in zip(acolcnt, pcolcnt):
    white += min(a, p)
  return (red, white)

def possibleAnswers(prevRounds):
  """Returns an iterable of all patterns which are consistent with responses to guesses thus far, provided as an array of (guess, (red, white))"""
  pr = tuple(prevRounds)
  return (candidate for candidate in allPatterns() if all((check(candidate, probe) == result for (probe, result) in pr)))

def randomPattern():
  """Select a random pattern"""
  return tuple((random.randint(0, COLORS - 1) for i in range(PINS)))

def chooseFirst(answers):
  """Pick the first response in the iterable answers"""
  guess = answers.next()
  answersCount = lambda: len(list(answers)) + 1
  return (guess, answersCount)

def chooseBest(answers):
  """Pick the best guess: the one that is likely to give the most information in its response
     (measured by it having the smallest peak in response concentration)""""
  allAnswers = list(answers)
  bestGuess = None
  bestScore = Math.pow(COLORS, PINS)
  bestResults = {}
  for guess in allAnswers:
    results = {}
    for possibleAnswer in allAnswers:
      possibleResult = check(possibleAnswer, guess)
      results[possibleResult] = 1 + results.get(possibleResult, 0)
    score = max(results.values())
    if score < bestScore:
      bestGuess = guess
      bestScore = score
      bestResults = results
  return (bestGuess, lambda: len(allAnswers))

def chooseRandom(answers):
  """Pick a possibly correct answer at random"""
  allAnswers = list(answers)
  guess = random.choice(allAnswers)
  return (guess, lambda: len(allAnswers))
  
def play(answer, chooser, onRound = None):
  """Play Mastermind once with the given answer and chooser"""
  rounds = []
  
  while 1:
    answers = possibleAnswers(rounds)
    (guess, answersCount) = chooser(answers)
    (red, white) = check(answer, guess)
    rounds.append((guess, (red, white)))
    if onRound:
      onRound(rounds, answersCount())
    if red == PINS:
      break
  
  return rounds

def printRound(rounds, answerCount):
  guess, (red, white) = rounds[-1]
  print "Round %d: %5d possible, guessed [%s], got %d red, %d white" % (len(rounds), answerCount, " ".join([str(v) for v in guess]), red, white)

def playOnce(chooser):
  answer = randomPattern()
  play(answer, chooser, onRound = printRound)

def playAll(chooser):
  results = {}
  for answer in allPatterns():
    rounds = play(answer, chooser)
    r = len(rounds)
    results[r] = 1 + results.get(r, 0)
  print "Rounds: Trials"
  for r in sorted(results.keys()):
    print "%-6d: %d" % (r, results[r])

CHOICES = {
  'first': chooseFirst,
  'best': chooseBest,
  'random': chooseRandom
}
CHOICES_HELP = ", ".join(CHOICES.keys())

def choiceType(arg):
  if arg in CHOICES:
    return CHOICES[arg]
  raise argparse.ArgumentTypeError("%s is unknown: valid choosers are [%s]" % 
    (arg, CHOICES_HELP))

def main(argv = None):
  global COLORS, PINS

  if argv is None:
    argv = sys.argv
  
  parser = argparse.ArgumentParser(description='Play Mastermind')
  parser.add_argument('--choose', type=choiceType, default=chooseFirst,
                      help='How to choose a move, one of [%s]' % CHOICES_HELP)
  parser.add_argument('--all', dest='action', action='store_const',
                      const=playAll, default=playOnce,
                      help='enumerate and summarize all Mastermind games')
  parser.add_argument('--colors', type=int, default=COLORS, help='Number of different colors each pin can have')
  parser.add_argument('--pins', type=int, default=PINS, help='Number of pins in the secret pattern')
  args = parser.parse_args(argv[1:])
  COLORS = args.colors
  PINS = args.pins
  
  args.action(chooser = args.choose)

if __name__ == "__main__":
  sys.exit(main())
