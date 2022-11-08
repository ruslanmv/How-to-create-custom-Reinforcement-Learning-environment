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

git clone 

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

