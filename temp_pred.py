<<<<<<< HEAD
import functions_framework
import torch
from transformers import BertTokenizer, BertForMaskedLM
from google.cloud import storage
import os
from os import path
from pathlib import Path

# https://classics-prediction-xkmqmbb5uq-uc.a.run.app

storage_client = storage.Client()
bucket = storage_client.get_bucket('classicsbucket')



# files = bucket.list_blobs()
# files = [file.name for file in files if '.' in file.name]
# greekberts = []
# for ii in files:
#      greekberts.append(str(ii))
# for ii in range(5):
#    greekberts.append(bucket.blob(files[ii]))

root = path.dirname(path.abspath(__file__))
os.mkdir("one")
os.mkdir("two")
os.mkdir("three")
os.mkdir("four")
os.mkdir("five")

tok = BertTokenizer.from_pretrained("pranaydeeps/Ancient-Greek-BERT")

blob = bucket.blob('1spanpsellos/pytorch_model.bin')
blob.download_to_filename('pytorch_model.bin')
Path("/workspace/pytorch_model.bin").rename("/workspace/one/pytorch_model.bin")
blob = bucket.get_blob('1spanpsellos/config.json')
blob.download_to_filename('config.json')
Path("/workspace/config.json").rename("/workspace/one/config.json")
greekbert1 = BertForMaskedLM.from_pretrained("/workspace/one")

blob = bucket.blob('3span_ft/pytorch_model.bin')
blob.download_to_filename('pytorch_model.bin')
Path("/workspace/pytorch_model.bin").rename("/workspace/two/pytorch_model.bin")
blob = bucket.blob('3span_ft/config.json')
blob.download_to_filename('config.json')
Path("/workspace/config.json").rename("/workspace/two/config.json")
greekbert2 = BertForMaskedLM.from_pretrained("/workspace/two")

blob = bucket.blob('3spanreal/pytorch_model.bin')
blob.download_to_filename('pytorch_model.bin')
Path("/workspace/pytorch_model.bin").rename("/workspace/three/pytorch_model.bin")
blob = bucket.blob('3spanreal/config.json')
blob.download_to_filename('config.json')
Path("/workspace/config.json").rename("/workspace/three/config.json")
greekbert3 = BertForMaskedLM.from_pretrained("/workspace/three")

blob = bucket.blob('4spanreal/pytorch_model.bin')
blob.download_to_filename('pytorch_model.bin')
Path("/workspace/pytorch_model.bin").rename("/workspace/four/pytorch_model.bin")
blob = bucket.blob('4spanreal/config.json')
blob.download_to_filename('config.json')
Path("/workspace/config.json").rename("/workspace/four/config.json")
greekbert4 = BertForMaskedLM.from_pretrained("/workspace/four")

blob = bucket.blob('5spanreal/pytorch_model.bin')
blob.download_to_filename('pytorch_model.bin')
Path("/workspace/pytorch_model.bin").rename("/workspace/five/pytorch_model.bin")
blob = bucket.blob('5spanreal/config.json')
blob.download_to_filename('config.json')
Path("/workspace/config.json").rename("/workspace/five/config.json")
greekbert5 = BertForMaskedLM.from_pretrained("/workspace/five")

greekberts = [greekbert1, greekbert2, greekbert3, greekbert4, greekbert5]

sm = torch.nn.Softmax(dim=1) # In order to construct word probabilities, we will employ softmax.
torch.set_grad_enabled(False) # Since we are not training, we disable gradient calculation.
sm = torch.nn.Softmax(dim=1) # In order to construct word probabilities, we will employ softmax.
torch.set_grad_enabled(False) # Since we are not training, we disable gradient calculation.

@functions_framework.http
def classicspred(request):
     request_json = request.get_json(silent=True)
     request_args = request.args
     # request json parsing
     if request_json and 'text' in request_json:
          text = request_json['text']
          text = text.decode("utf-16")
     else:
          text = 'return valid text'
          return text
     if request_json and 'suffix' in request_json:
          suffix = request_json['suffix']
     else:
          suffix = ""
     if request_json and 'prefix' in request_json:
          prefix = request_json['prefix']
     else:
          prefix = ""
     if request_json and 'num_pred' in request_json:
          num_pred = request_json['num_pred']
     else:
          num_pred = 5
     
     # request args 
     if request_args and 'text' in request_args:
          text = request_args['text']
          text = text.decode("utf-16")
     else:
          text = 'return valid text'
          return text
     if request_args and 'suffix' in request_args:
          suffix = request_args['suffix']
     else:
          suffix = ""
     if request_args and 'prefix' in request_args:
          prefix = request_args['prefix']
     else:
          prefix = ""
     if request_args and 'num_pred' in request_args:
          num_pred = request_args['num_pred']

     else:
          num_pred = 5
     parameters = {
        'prefix' : prefix,
        'suffix' : suffix,
        'num_pred' : num_pred,
        }
     
     # parameters = {
     #      'prefix' : 'ε',
     #      'suffix' : None,
     #      'num_pred' : 5,
     # }
     # text = f'Πρῶτον {tok.mask_token} περὶ τί καὶ τίνος ἐστὶν ἡ σκέψις, ὅτι περὶ ἀπόδειξιν καὶ ἐπιστήμης ἀποδεικτικῆς· εἶτα διορίσαι τί ἐστι πρότασις καὶ τί ὅρος καὶ τί συλλογισμός, καὶ ποῖος τέλειος καὶ ποῖος ἀτελής, μετὰ δὲ ταῦτα τί τὸ ἐν ὅλῳ εἶναι ἢ μὴ εἶναι τόδε τῷδε, καὶ τί λέγομεν τὸ κατὰ παντὸς ἢ μηδενὸς κατηγορεῖσθαι.'
#    return list_files()
     ret = main(text, parameters)
     return ret

def list_files():
     root = path.dirname(path.abspath(__file__))
     children = os.listdir(root)
     # files = [c for c in children if path.isfile(path.join(root, c))]
     ret = []
     for ii in children:
          if path.isfile(path.join(root, ii)):
               ret.append("True")
          else:
               ret.append("False")
     ret.append(root)
#         ret.append(files)
     return ret

# def list_blobs():
#    """Lists all the blobs in the bucket."""
#    bucket_name = "classicsbucket"

#    storage_client = storage.Client()

#    # Note: Client.list_blobs requires at least package version 1.17.0.
#    blobs = storage_client.list_blobs(bucket_name)

#    # Note: The call returns a response only when the iterator is consumed.
#    ret = []
#    for blob in blobs:
#           ret.append(blob.name)
#    return ret

# Get top 5 suggestions for each masked position:
def argkmax(array, k, prefix='', dim=0): # Return indices of the 1st through kth largest values of an array
     indices = []
     new_prefixes = []
     added = 0
     ind = 1
     while added < k:
          if ind > len(array[0]):
               break
          val = torch.kthvalue(-array, ind, dim=dim).indices.numpy().tolist()
          if prefix != '':
               cur_tok = tok.convert_ids_to_tokens(val[0]).replace('##', '')
               trunc_prefix = prefix[:min(len(prefix), len(cur_tok))]
          if not cur_tok.startswith(trunc_prefix):
               ind += 1
               continue
          else:
               cur_tok = ''
          indices.append(val)
          if len(cur_tok) >= len(prefix):
               new_prefixes.append('')
          else:
               new_prefixes.append(prefix[len(cur_tok):])
          ind += 1
          added += 1
     return torch.tensor(indices), new_prefixes

# gets n predictions / probabilities for a single masked token , by default, the first masked token
def get_n_preds(token_ids, n, prefix, masked_ind, fill_inds, cur_prob=1):
     mask_positions = (token_ids.squeeze() == tok.mask_token_id).nonzero().flatten().tolist()
     for i in range(len(fill_inds)):
          token_ids.squeeze()[mask_positions[i]] = fill_inds[i]

    #print(len(mask_positions), len(fill_inds))
     model_id = min(len(mask_positions) - len(fill_inds) - 1, 4)
   #print(model_id)
     greekbert = greekberts[model_id]
     logits = greekbert(token_ids).logits.squeeze(0)
     mask_logits = logits[[[masked_ind]]]
     probabilities = sm(mask_logits)
     arg1, prefixes = argkmax(probabilities, n, prefix, dim=1)
     suggestion_ids = arg1.squeeze().tolist()
     n_probs = probabilities.squeeze()[suggestion_ids]
     n_probs = torch.mul(n_probs, cur_prob).tolist()
     new_fill_inds = [fill_inds + [i] for i in suggestion_ids]
     return tuple(zip(new_fill_inds, n_probs, prefixes)) 

def beam_search(token_ids, beam_size, prefix=''):
     mask_positions = (token_ids.detach().clone().squeeze() == tok.mask_token_id).nonzero().flatten().tolist()
   # print(len(mask_positions))
     num_masked = len(mask_positions)
     cur_preds = get_n_preds(token_ids.detach().clone(), beam_size, prefix, mask_positions[0], [])
   # for c in range(len(cur_preds)):
        # print(tok.convert_ids_to_tokens(cur_preds[c][0][0]))

     for i in range(num_masked - 1):
        # print(i)
          candidates = []
          for j in range(len(cur_preds)):
               candidates += get_n_preds(token_ids.detach().clone(), 20, cur_preds[j][2], mask_positions[i + 1], cur_preds[j][0], cur_preds[j][1])
          candidates.sort(key=lambda k:k[1],reverse=True)
          cur_preds = candidates[:beam_size]
     return cur_preds

  # Get top 5 suggestions for each masked position:
def argkmax_right(array, k, suffix='', dim=0): # Return indices of the 1st through kth largest values of an array
     indices = []
     new_suffixes = []
     added = 0
     ind = 1
     while added < k:
          if ind > len(array[0]):
               break
          val = torch.kthvalue(-array, ind, dim=dim).indices.numpy().tolist()
          if suffix != '':
               cur_tok = tok.convert_ids_to_tokens(val[0]).replace('##', '')
               trunc_suffix = suffix[len(suffix) - min(len(suffix), len(cur_tok)):]
               if not cur_tok.endswith(trunc_suffix):
                    ind += 1
                    continue
          else:
               cur_tok = ''
          indices.append(val)
          if len(cur_tok) >= len(suffix):
               new_suffixes.append('')
          else:
               new_suffixes.append(suffix[:len(suffix) - len(cur_tok)])
          ind += 1
          added += 1
     return torch.tensor(indices), new_suffixes

# gets n predictions / probabilities for a single masked token , by default, the first masked token
def get_n_preds_right(token_ids, n, suffix, masked_ind, fill_inds, cur_prob=1):
     mask_positions = (token_ids.squeeze() == tok.mask_token_id).nonzero().flatten().tolist()
     # fill in the current guessed tokens
     for i in range(len(fill_inds)):
          token_ids.squeeze()[mask_positions[len(mask_positions) - i - 1]] = fill_inds[i]
     #print(len(mask_positions), len(fill_inds))
     model_id = min(len(mask_positions) - len(fill_inds) - 1, 4)
     #print(model_id)
     greekbert = greekberts[model_id]
     logits = greekbert(token_ids).logits.squeeze(0)
     mask_logits = logits[[[masked_ind]]]
     probabilities = sm(mask_logits)
     arg1, suffixes = argkmax_right(probabilities, n, suffix, dim=1)
     suggestion_ids = arg1.squeeze().tolist()
     n_probs = probabilities.squeeze()[suggestion_ids]
     n_probs = torch.mul(n_probs, cur_prob).tolist()
     new_fill_inds = [fill_inds + [i] for i in suggestion_ids]
     return tuple(zip(new_fill_inds, n_probs, suffixes)) 

def beam_search_right(token_ids, beam_size, suffix=''):
     mask_positions = (token_ids.detach().clone().squeeze() == tok.mask_token_id).nonzero().flatten().tolist()
     num_masked = len(mask_positions)
     cur_preds = get_n_preds_right(token_ids.detach().clone(), beam_size, suffix, mask_positions[-1], [])
     for c in range(len(cur_preds)):
          print(tok.convert_ids_to_tokens(cur_preds[c][0][0]))
     for i in range(num_masked - 1, 0, -1):
          print(i)
          candidates = []
          for j in range(len(cur_preds)):
               candidates += get_n_preds_right(token_ids.detach().clone(), 100, cur_preds[j][2], mask_positions[i - 1], cur_preds[j][0], cur_preds[j][1])
          candidates.sort(key=lambda k:k[1],reverse=True)
          if i != 1:
               cur_preds = candidates[:beam_size]
          else:
               cur_preds = candidates
     return cur_preds

# Wrapper method 
def main(text, parameters):
     suffix = parameters['suffix']
     prefix = parameters['prefix']
     num_pred = parameters['num_pred']
     if suffix and prefix is None:
          return
     # Defaults to suffix prediction first (if both are filled out)
     if suffix is not None:
          tokens = tok.encode(text, return_tensors = 'pt')
          results = beam_search_right(tokens, num_pred, suffix)
     else:
          tokens = tok.encode(text, return_tensors = 'pt')
          results = beam_search(tokens, num_pred, prefix)
     ret = []
     for row in results:
          # row[0] stores the token_id
          temp = tok.convert_ids_to_tokens(row[0])
          # row[1] stores the probability
          row_format = [temp, row[1]]
          ret.append(row_format)
     return ret
=======
# installing required dependencies
import torch
from transformers import BertTokenizer, BertForMaskedLM
# may need to do pip install transformers
# may need to do pip install torch
# files needed to do predictions.
# https://drive.google.com/drive/u/2/folders/1eocoWpyd8NdrQATGwV47dqUnRQvtxhII

tok = BertTokenizer.from_pretrained("pranaydeeps/Ancient-Greek-BERT")
greekbert1 = BertForMaskedLM.from_pretrained("1spanpsellos")
greekbert2 = BertForMaskedLM.from_pretrained("3span_ft")
greekbert3 = BertForMaskedLM.from_pretrained("3spanreal")
greekbert4 = BertForMaskedLM.from_pretrained("4spanreal")
greekbert5 = BertForMaskedLM.from_pretrained("5spanreal")

# greekbert1.eval() # We are not training BERT at all here, only evaluating it. Thus we call bert.eval().
# greekbert2.eval() # We are not training BERT at all here, only evaluating it. Thus we call bert.eval().
# greekbert3.eval() # We are not training BERT at all here, only evaluating it. Thus we call bert.eval().
# greekbert4.eval() # We are not training BERT at all here, only evaluating it. Thus we call bert.eval().
# greekbert5.eval() # We are not training BERT at all here, only evaluating it. Thus we call bert.eval().

greekberts = [greekbert1, greekbert2, greekbert3, greekbert4, greekbert5]
sm = torch.nn.Softmax(dim=1) # In order to construct word probabilities, we will employ softmax.
torch.set_grad_enabled(False) # Since we are not training, we disable gradient calculation.

# Get top 5 suggestions for each masked position:
def argkmax(array, k, prefix='', dim=0): # Return indices of the 1st through kth largest values of an array
    indices = []
    new_prefixes = []
    added = 0
    ind = 1
    while added < k:
        if ind > len(array[0]):
            break
        val = torch.kthvalue(-array, ind, dim=dim).indices.numpy().tolist()
        if prefix != '':
            cur_tok = tok.convert_ids_to_tokens(val[0]).replace('##', '')
            trunc_prefix = prefix[:min(len(prefix), len(cur_tok))]
            if not cur_tok.startswith(trunc_prefix):
                ind += 1
                continue
        else:
            cur_tok = ''
        indices.append(val)
        if len(cur_tok) >= len(prefix):
            new_prefixes.append('')
        else:
            new_prefixes.append(prefix[len(cur_tok):])
        ind += 1
        added += 1
    return torch.tensor(indices), new_prefixes

# gets n predictions / probabilities for a single masked token , by default, the first masked token
def get_n_preds(token_ids, n, prefix, masked_ind, fill_inds, cur_prob=1):
    mask_positions = (token_ids.squeeze() == tok.mask_token_id).nonzero().flatten().tolist()
    for i in range(len(fill_inds)):
        token_ids.squeeze()[mask_positions[i]] = fill_inds[i]

    #print(len(mask_positions), len(fill_inds))
    model_id = min(len(mask_positions) - len(fill_inds) - 1, 4)
    #print(model_id)
    greekbert = greekberts[model_id]
    logits = greekbert(token_ids).logits.squeeze(0)
    mask_logits = logits[[[masked_ind]]]
    probabilities = sm(mask_logits)
    arg1, prefixes = argkmax(probabilities, n, prefix, dim=1)
    suggestion_ids = arg1.squeeze().tolist()
    n_probs = probabilities.squeeze()[suggestion_ids]
    n_probs = torch.mul(n_probs, cur_prob).tolist()
    new_fill_inds = [fill_inds + [i] for i in suggestion_ids]
    return tuple(zip(new_fill_inds, n_probs, prefixes)) 

def beam_search(token_ids, beam_size, prefix=''):
    mask_positions = (token_ids.detach().clone().squeeze() == tok.mask_token_id).nonzero().flatten().tolist()
    # print(len(mask_positions))
    num_masked = len(mask_positions)
    cur_preds = get_n_preds(token_ids.detach().clone(), beam_size, prefix, mask_positions[0], [])
    # for c in range(len(cur_preds)):
        # print(tok.convert_ids_to_tokens(cur_preds[c][0][0]))

    for i in range(num_masked - 1):
        # print(i)
        candidates = []
        for j in range(len(cur_preds)):
            candidates += get_n_preds(token_ids.detach().clone(), 20, cur_preds[j][2], mask_positions[i + 1], cur_preds[j][0], cur_preds[j][1])
        candidates.sort(key=lambda k:k[1],reverse=True)
        cur_preds = candidates[:beam_size]
    return cur_preds

  # Get top 5 suggestions for each masked position:
def argkmax_right(array, k, suffix='', dim=0): # Return indices of the 1st through kth largest values of an array
    indices = []
    new_suffixes = []
    added = 0
    ind = 1
    while added < k:
        if ind > len(array[0]):
            break
        val = torch.kthvalue(-array, ind, dim=dim).indices.numpy().tolist()
        if suffix != '':
            cur_tok = tok.convert_ids_to_tokens(val[0]).replace('##', '')
            trunc_suffix = suffix[len(suffix) - min(len(suffix), len(cur_tok)):]
            if not cur_tok.endswith(trunc_suffix):
                ind += 1
                continue
            else:
                cur_tok = ''
        indices.append(val)
        if len(cur_tok) >= len(suffix):
            new_suffixes.append('')
        else:
            new_suffixes.append(suffix[:len(suffix) - len(cur_tok)])
        ind += 1
        added += 1
    return torch.tensor(indices), new_suffixes

# gets n predictions / probabilities for a single masked token , by default, the first masked token
def get_n_preds_right(token_ids, n, suffix, masked_ind, fill_inds, cur_prob=1):
    mask_positions = (token_ids.squeeze() == tok.mask_token_id).nonzero().flatten().tolist()
    # fill in the current guessed tokens
    for i in range(len(fill_inds)):
        token_ids.squeeze()[mask_positions[len(mask_positions) - i - 1]] = fill_inds[i]
    #print(len(mask_positions), len(fill_inds))
    model_id = min(len(mask_positions) - len(fill_inds) - 1, 4)
    #print(model_id)
    greekbert = greekberts[model_id]
    logits = greekbert(token_ids).logits.squeeze(0)
    mask_logits = logits[[[masked_ind]]]
    probabilities = sm(mask_logits)
    arg1, suffixes = argkmax_right(probabilities, n, suffix, dim=1)
    suggestion_ids = arg1.squeeze().tolist()
    n_probs = probabilities.squeeze()[suggestion_ids]
    n_probs = torch.mul(n_probs, cur_prob).tolist()
    new_fill_inds = [fill_inds + [i] for i in suggestion_ids]
    return tuple(zip(new_fill_inds, n_probs, suffixes)) 

def beam_search_right(token_ids, beam_size, suffix=''):
  mask_positions = (token_ids.detach().clone().squeeze() == tok.mask_token_id).nonzero().flatten().tolist()
  num_masked = len(mask_positions)
  cur_preds = get_n_preds_right(token_ids.detach().clone(), beam_size, suffix, mask_positions[-1], [])
  for c in range(len(cur_preds)):
    print(tok.convert_ids_to_tokens(cur_preds[c][0][0]))
    for i in range(num_masked - 1, 0, -1):
        print(i)
        candidates = []
        for j in range(len(cur_preds)):
            candidates += get_n_preds_right(token_ids.detach().clone(), 100, cur_preds[j][2], mask_positions[i - 1], cur_preds[j][0], cur_preds[j][1])
    candidates.sort(key=lambda k:k[1],reverse=True)
    if i != 1:
        cur_preds = candidates[:beam_size]
    else:
        cur_preds = candidates
  return cur_preds

# Wrapper method 
def main(text, parameters):
    # returns if there is no prefix or suffix to be filled out
    suffix = parameters['suffix']
    prefix = parameters['prefix']
    num_pred = parameters['num_pred']

    if suffix and prefix is None:
        return
    # Defaults to suffix prediction first (if both are filled out)
    if suffix is not None:
        tokens = tok.encode(text, return_tensors = 'pt')
        results = beam_search_right(tokens, num_pred, suffix)
    else:
        tokens = tok.encode(text, return_tensors = 'pt')
        results = beam_search(tokens, num_pred, prefix)
    ret = []
    for row in results:
        # row[0] stores the token_id
        temp = tok.convert_ids_to_tokens(row[0])
        # row[1] stores the probability
        row_format = [temp, row[1]]
        ret.append(row_format)
    return ret

if __name__ == '__main__':
    main()
    # # test input
    # parameters = {
    #     'prefix' : 'ε',
    #     'suffix' : None,
    #     'num_pred' : 20
    #     }

    # orig_text = f"""Πρῶτον εἰπεῖν περὶ τί καὶ τίνος ἐστὶν ἡ σκέψις, ὅτι περὶ ἀπόδειξιν καὶ ἐπιστήμης ἀποδεικτικῆς· εἶτα διορίσαι τί ἐστι πρότασις καὶ τί ὅρος καὶ τί συλλογισμός, καὶ ποῖος τέλειος καὶ ποῖος ἀτελής, μετὰ δὲ ταῦτα τί τὸ ἐν ὅλῳ εἶναι ἢ μὴ εἶναι τόδε τῷδε, καὶ τί λέγομεν τὸ κατὰ παντὸς ἢ μηδενὸς κατηγορεῖσθαι."""
    # text = f"""Πρῶτον {tok.mask_token} {tok.mask_token} περὶ τί καὶ τίνος ἐστὶν ἡ σκέψις, ὅτι περὶ ἀπόδειξιν καὶ ἐπιστήμης ἀποδεικτικῆς· εἶτα διορίσαι τί ἐστι πρότασις καὶ τί ὅρος καὶ τί συλλογισμός, καὶ ποῖος τέλειος καὶ ποῖος ἀτελής, μετὰ δὲ ταῦτα τί τὸ ἐν ὅλῳ εἶναι ἢ μὴ εἶναι τόδε τῷδε, καὶ τί λέγομεν τὸ κατὰ παντὸς ἢ μηδενὸς κατηγορεῖσθαι."""

    # output = main(text, parameters)
    # print (output)
>>>>>>> 0b75ce029b01d023df855af716a7c6171b136555
