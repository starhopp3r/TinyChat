# TinyChat

TinyChat15M is a 15-million parameter conversational language model built on the Meta Llama 2 architecture. Designed to operate on devices with as little as 60 MB of free memory, TinyChat15M has been successfully deployed on the Sipeed LicheeRV Nano W, a compact RISC-V development board equipped with just 256 MB of DDR3 memory. Inspired by Dr. Andrej Karpathy’s llama2.c project, TinyChat15M showcases that small conversational language models can be both effective and resource-efficient, making advanced AI capabilities more accessible and sustainable. You can find a detailed blog post on this project [here](https://nikhilr.io/posts/TinyChat15M/).

## Usage

First, navigate to the folder where you keep your projects, and then clone this repository into that folder:

```
git clone https://github.com/starhopp3r/TinyChat.git
```

Next, navigate to the llama2.c folder:

```
cd llama2.c
```

Now, download the TinyChat15M model from Hugging Face:

```
wget https://huggingface.co/starhopp3r/TinyChat/resolve/main/TinyChat15M.bin
```

Next, compile the C code:

```
make run
```

Now, to run the TinyChat15M Assistant use the following command:

```
./run TinyChat15M -t 1.0 -p 0.9 -n 2048 -m chat
```

Note that the temperature (`-t` flag) and top-p value (`-p` flag) can be set to any number between `0` and `1`. For optimal results, it's recommended to sample with `-t 1.0` and `-p 0.9`, meaning a temperature of `1.0` (default) and top-p sampling at `0.9` (default). Intuitively, top-p sampling prevents tokens with extremely low probabilities from being selected, reducing the chances of getting "unlucky" during sampling and decreasing the likelihood of generating off-topic content. Generally, to control the diversity of samples, you can either adjust the temperature (i.e., vary `-t` between `0` and `1` while keeping top-p off with `-p 0`) or the top-p value (i.e., vary `-p` between `0` and `1` while keeping the temperature at `1`), but it’s advisable not to modify both simultaneously. Detailed explanations of LLM sampling strategies can be found [here](https://peterchng.com/blog/2023/05/02/token-selection-strategies-top-k-top-p-and-temperature/), [here](https://docs.cohere.com/docs/controlling-generation-with-top-k-top-p) and [here](https://huggingface.co/blog/how-to-generate).
