from torch import no_grad
from torch.utils.data import DataLoader


"""
Functions you should use.
Please avoid importing any other functions or modules.
Your code will not pass if the gradescope autograder detects any changed imports
"""
from torch import optim, tensor
from losses import regression_loss, digitclassifier_loss, languageid_loss, digitconvolution_Loss
from torch import movedim


"""
##################
### QUESTION 1 ###
##################
"""


def train_perceptron(model, dataset):
    """
    Train the perceptron until convergence.
    You can iterate through DataLoader in order to 
    retrieve all the batches you need to train on.

    Each sample in the dataloader is in the form {'x': features, 'label': label} where label
    is the item we need to predict based off of its features.
    """
    with no_grad():
        dataloader = DataLoader(dataset, batch_size=1, shuffle=True)
        "*** YOUR CODE HERE ***"
        converged = False
        while not converged:
            converged = True
            for batch in dataloader:
                x, y = batch['x'], batch['label'].item()
                if model.get_prediction(x) != y:
                    model.w += y * x
                    converged = False


def train_regression(model, dataset):
    """
    Trains the model.

    In order to create batches, create a DataLoader object and pass in `dataset` as well as your required 
    batch size. You can look at PerceptronModel as a guideline for how you should implement the DataLoader

    Each sample in the dataloader object will be in the form {'x': features, 'label': label} where label
    is the item we need to predict based off of its features.

    Inputs:
        model: Pytorch model to use
        dataset: a PyTorch dataset object containing data to be trained on
        
    """
    "*** YOUR CODE HERE ***"
    batch_size = 20                      # 200 examples -> divides evenly
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    optimizer = optim.Adam(model.parameters(), lr=0.002)
    target_loss = 0.005                  # well below the 0.02 threshold
    for epoch in range(2000):
        total_loss = 0.0
        for batch in dataloader:
            optimizer.zero_grad()
            loss = regression_loss(model(batch['x']), batch['label'])
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * len(batch['x'])
        if total_loss / len(dataset) < target_loss:
            break


def train_digitclassifier(model, dataset):
    """
    Trains the model.
    """
    model.train()
    """ YOUR CODE HERE """
    batch_size = 100                     # 60000 examples -> divides evenly
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    for epoch in range(20):
        for batch in dataloader:
            optimizer.zero_grad()
            loss = digitclassifier_loss(model(batch['x']), batch['label'])
            loss.backward()
            optimizer.step()
        # Test accuracy is graded at 97%, so stop with some margin on validation.
        if dataset.get_validation_accuracy() >= 0.985:
            break


def train_languageid(model, dataset):
    """
    Trains the model.

    Note that when you iterate through dataloader, each batch will returned as its own vector in the form
    (batch_size x length of word x self.num_chars). However, in order to run multiple samples at the same time,
    get_loss() and run() expect each batch to be in the form (length of word x batch_size x self.num_chars), meaning
    that you need to switch the first two dimensions of every batch. This can be done with the movedim() function 
    as follows:

    movedim(input_vector, initial_dimension_position, final_dimension_position)

    For more information, look at the pytorch documentation of torch.movedim()
    """
    model.train()
    "*** YOUR CODE HERE ***"
    batch_size = 32
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    for epoch in range(20):
        for batch in dataloader:
            xs = movedim(batch['x'], 0, 1)   # (batch, length, chars) -> (length, batch, chars)
            optimizer.zero_grad()
            loss = languageid_loss(model(xs), batch['label'])
            loss.backward()
            optimizer.step()
        if dataset.get_validation_accuracy() >= 0.86:
            break



def Train_DigitConvolution(model, dataset):
    """
    Trains the model.
    """
    """ YOUR CODE HERE """
    batch_size = 10
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    for epoch in range(30):
        for batch in dataloader:
            optimizer.zero_grad()
            loss = digitconvolution_Loss(model(batch['x']), batch['label'])
            loss.backward()
            optimizer.step()
        if dataset.get_validation_accuracy() >= 0.9:
            break
