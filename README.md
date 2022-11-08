# How to create a custom Reinforcement Learning Environment in Gym



## Step 1. Creation of  Python environment

I will create an environment called **gym**, because we are interested in the **Gymnasium** library.

Gymnasium is **an open source Python library for developing and comparing reinforcement learning algorithms** by providing a standard API to communicate between learning algorithms and environments, as well as a standard set of environments compliant with that API. 

First you need to install anaconda at this [link](https://www.anaconda.com/products/individual)

then after is installed type in your terminal

```
conda create -n gym python==3.7
```

then

```
conda activate gym
```

then we install the following libraries

```
pip install   gym==0.18.0 keras notebook  pygame matplotlib tensorflow  keras-rl2
```

hen in your terminal type the following commands:

```
conda install ipykernel
```

then we install

```
python -m ipykernel install --user --name gym --display-name "Python (Gym)"
```

and then  we clone our repository

```
git clone https://github.com/ruslanmv/How-to-create-custom-Reinforcement-Learning-environment.git
```



```
cd How-to-create-custom-Reinforcement-Learning-environment
```

```
pip install -e snake
```

<img src="assets/images/posts/README/image-20221108204035363.png" alt="image-20221108204035363" style="zoom:50%;" />



then we type

```
jupyter notebook
```



and we choose our Python (Gym) notebook

![image-20221108202558247](assets/images/posts/README/image-20221108202558247.png)

If you want to uninstall your environment

```
conda env remove -n gym
```

and by typing

```
jupyter kernelspec list
```

 to get the paths of all your kernels.
Then simply uninstall your unwanted-kernel

```
jupyter kernelspec uninstall gym
```



# Creating an Open AI Gym Environment

Once is loaded the Python (Gym) kernel  you can open the example notebooks.

The first notebook, is simple the game  where we want to develop the appropriate enviroment

 [0-Custom-Snake-Game.ipynb](https://github.com/ruslanmv/How-to-create-custom-Reinforcement-Learning-environment/blob/master/0-Custom-Snake-Game.ipynb)

The second notebook is an example about how to initialize the custom environment,

that has the structure

<img src="assets/images/posts/README/image-20221108230436802.png" alt="image-20221108230436802" style="zoom:50%;" />

in our case 

<img src="assets/images/posts/README/image-20221108230519054.png" alt="image-20221108230519054" style="zoom:50%;" />

[1-Creating-a-Gym-Environment.ipynb](https://github.com/ruslanmv/How-to-create-custom-Reinforcement-Learning-environment/blob/master/1-Creating-a-Gym-Environment.ipynb)

and finally the third notebook is simply an application of the Gym Environment into a RL model.

[2-Applying-a-Custom-Environment.ipyn](https://github.com/ruslanmv/How-to-create-custom-Reinforcement-Learning-environment/blob/master/2-Applying-a-Custom-Environment.ipynb)