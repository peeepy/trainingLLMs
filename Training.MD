# Training LLMs
This is a step-by-step guide to training an LLM. While it is not exactly the same process, I am accompanying it with a notebook guiding you through the LoRA finetuning process and inference. With that, I have a LoRA-finetuned LLaMa 7B trained on Roleplaying Guild data I cleaned and processed, and trained using the notebook. This was trained over an hour using 1x A100-80G. You can find the LoRA in the 'LoRA' folder.

## Short guide
1. Gather and process data.\
    a. Determine the type of data you want to train on\
    b. Scrape or gather data\
    c. Process the data - perform deduplication, parse the data, convert to an appropriate format (e.g .csv > .json)\
    d. Tokenize the data so that it's ready for training
2. Train the model on the data.\
    a. Set hyperparameters:
        i. Batch size - The number of data points that are processed together in one iteration of the training process.\
        ii. Micro-batch size - The number of data chunks that are processed together in one back-and-forward pass of the neural network. Using microbatches can help reduce VRAM usage during training.\
        iii. Learning rate - The learning rate determines the step size taken during gradient descent and can significantly affect training performance.\
        iv. Steps - The number of training steps determines how long the model is trained for. Too few training steps can result in underfitting (unable to detect patterns in the data), while too many can lead to overfitting ('memorising' the training data so that it does poorly on new data).\
    b. Choose your optimisation algorithm:
        i. Adam optimisation - a mix of Gradient Descent and Stochastic Gradient Descent (SGD) that keeps an average of the gradient & gradient squared and uses this information to adjust the learning rate. Often results in a faster convergence and better performance.\
        ii. Gradient descent - This algorithm updates the model's parameters in the direction of the steepest descent of the loss function. This means that it adjusts the parameters to reduce the loss as quickly as possible.\
        iii. Stochastic gradient descent (SGD): SGD is a variant of gradient descent that randomly selects a single sample from the training set and calculates the gradient based on that sample. This makes SGD faster than batch gradient descent, but it can also be less accurate since it relies on a single sample to update the parameters.\
    c. Split the data into **train** and **validation** sets\
    d. Train the model with the chosen hyperparameters and optimisation algorithm\
        i. During training, test the model using the eval (validation) set to determine its performance and adjust hyperparameters as necessary\
    e. Perform inference with the trained model to test its performance.


## Verbose guide
### Data
#### Gathering and processing data
The most important step in training an LLM is the data you gather. If you want a model that can generate code for you, or help you debug your code, you'll want to train it on a lot of code data; if you want a model trained on chatting for roleplaying purposes, you'll want the model trained on a lot of dialogue so that it knows how to act in a roleplay scenario.

The amount of data you need is variable. For training from scratch, a lot of people use The Pile to form a good base. **The Pile** is a very large dataset (800+GB) that covers a large, diverse dataset of books, Wikipedia articles, etc.

Some popular places to gather data are:\
[Huggingface](https://huggingface.co/datasets)\
[Kaggle](https://www.kaggle.com/datasets)\
[Google Dataset Search](https://datasetsearch.research.google.com/)

If you're looking to train your LLM on something specific, chances are you're going to need to scrape your own data as well.
Many scrapers exist for different sites, such as Reddit and various Light Novels. Usually, scrapers first extract the text from a site in raw HTML, then the data is *parsed*; the plain text and other useful aspects (such as titles, usernames, etc) are taken from the raw HTML to begin cleaning the data.

Often, pre-scraped data is formatted into .csv files that will need to be converted to .json/.jsonl for training after processing them as explained below. It's usually easier to follow the process of **scraped data -> .csv -> .json** when dealing with data gathering.

Parsing also involves breaking the text down into more manageable chunks (for 2048 context models, ensuring the input sequence is no more than 2048 tokens, for example).
To clean data effectively, you want to ensure you're removing any unnecessary content that is causing bloat and could lower the quality of the data. This includes (and is not exhaustive):
* Deduplicating - removing duplicate data
* Unnecessary words - could increase the token amount unnecessarily
* Correcting spelling mistakes
* Removing irrelevant content (e.g incomplete code in the case of coding data, some OOC in roleplaying data)

While scraping data, ensure you follow legal guidelines as some data could be illegal to scrape and/or come with ethical concerns (scraping private websites, for example).
Perhaps most importantly, the data must be **diverse** within its chosen topic(s). This will ensure the model can generate varied, unique, accurate text. A dataset with a small amount of diversity could introduce biases to the model and lead to low quality generations.

#### Tokenizing data
All data must be tokenized to prepare it for training. In tokenization, a tokenizer is used (in finetuning, the base model tokenizer) to split the input sequences into small chunks of text that is model-readable to allow it to be trained. Tokenization also involves assigning each token a unique integer identifier or index, also known as tensors, that the model can read and understand.

Tokenization is an essential step in training any language model because it helps to standardize the input data and make it more consistent. By breaking the text down into smaller, more manageable units, the model can learn to recognize patterns and relationships between the different tokens, which is important certain tasks such as language generation, machine translation, and sentiment analysis.

### Training
Before you begin training the model, there are some hyperparameters that must be set and a decision to be made on the optimisation algorithm.\
**Hyperparameters**
* Batch size: The number of data points that are processed together in one iteration of the training process. A large batch size can speed up training by allowing for parallelization on GPUs, but it also requires more memory. A common rule of thumb is to use the largest batch size that can fit in memory. However, smaller batch sizes can sometimes improve generalization by introducing more noise into the optimization process.

* Micro-batch size: The number of data chunks that are processed together in one back-and-forward pass of the neural network. It is a way to break down large batches of data into smaller, more manageable chunks. For example, if you have a batch size of 128 and a microbatch size of 4, the 128 examples in the batch will be processed in 32 microbatches of 4 examples each. Using microbatches can help reduce memory usage during training.

* Learning rate: The learning rate determines the step size taken during gradient descent and can significantly affect training performance. A common method is to start with a small learning rate and gradually increase it until convergence (when the model has learned all it can from the data and further training won't improve its performance) or until the loss stops improving. Learning rate schedules can also be used to adjust the learning rate during training.

* Number of training steps: The number of training steps determines how long the model is trained for. Too few training steps can result in underfitting (unable to detect patterns in the data), while too many can lead to overfitting ('memorising' the training data so that it does poorly on new data). A common rule of thumb is to monitor the loss on a validation set and stop training when it starts to increase.

**Optimisation algorithms**
* Adam optimiser: This is the most common optimisation algorithm used as it combines the advantages of **Gradient descent** and **Stochastic gradient descent (SGD)**. It keeps a moving average of the gradient & gradient squared and uses this information to adjust the learning rate  for each parameter during training. This can result in faster convergence and better model performance.
* Gradient descent: This algorithm updates the model's parameters in the direction of the steepest descent of the loss function. This means that it adjusts the parameters to reduce the loss as quickly as possible. There are different variants, such as batch gradient descent, which updates the parameters using the entire dataset, and mini-batch gradient descent, which updates the parameters using a sample of the data.
* Stochastic gradient descent (SGD): SGD is a variant of gradient descent that randomly selects a single sample from the training set and calculates the gradient based on that sample. This makes SGD faster than batch gradient descent, but it can also be less accurate since it relies on a single sample to update the parameters.

Most developers use **Adam optimising** as it often results in better performance and faster training.

## Training the model
Once the data has been processed and tokenized, and the hyperparameters have been set, training can begin.
The data is usually split into **train** and **eval** datasets. The **train** dataset is the data that the model gets trained on. The **eval** (or validation) set is another chunk of data that the model is evaluated on throughout training to allow the developers to adjust hyperparameters as needed. A lot of developers also use **test** sets with unseen data to test the performance of the model post-training.

During training, the model is fed batches of training data and the forward pass is performed to make predictions for each batch. The predictions are then compared to the actual labels of the data using a loss function, which computes a measure of how far off the predictions are from the true values.\
The backpropagation algorithm is then used to calculate the gradient of the loss function with respect to the model's parameters (i.e., the weights and biases). This gradient is used to update the model's parameters in the opposite direction of the gradient, which is meant to decrease the loss.\
The size of the update to the parameters is determined by the learning rate. This process is repeated for each batch of data until all the training data has been processed. One pass through the entire dataset is called an epoch. Typically, multiple epochs are performed to allow the model to see each example multiple times and make incremental improvements to its predictions.\
Training ends when the stop criterion has been met; typically this is a certain number of epochs, convergence of loss, or the accuracy of the model based on the validation set.