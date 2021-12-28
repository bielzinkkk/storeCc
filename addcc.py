import json 

i = open("sample.txt", "r")
samples = i.read()

def split_card(card) -> dict:
  splited = card.split("|")
  return {
    
  }
  
cards = [split_card(card) for card in samples.strip().split("\n")]
print(tuple(cards))