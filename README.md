# basketball-evals
Learning inspect by creating simple evals related to basketball

## Results

### Basketball Plays Questions

| Model | Setting | Accuracy | Std Error |
|-------|---------|----------|-----------|
| llama3.2 | Zero-shot | 0.320 | 0.067 |
| llama3.2 | Few-shot | 0.420 | 0.071 |
| llama3.2:1b | Zero-shot | 0.360 | 0.069 |
| llama3.2:1b | Few-shot | 0.220 | 0.059 |


### Thoughts on results
Tested using llama3.2 and lama3.2:1b locally on 1 epoch with the temperature set to 0. llama3.2 was more accurate when given fewshot examples, however 3.2:1b was less accurate when given fewshot examples. I think because 3.2:1b is a smaller model it may struggle with few-shot examples for a variety of reasons such as context dilution and difficulty following instructions. When I tried reducing the number of few-shots to 1 the accuracy seems to go up to 0.260.

I was also surprised that 3.2 preformed worse than 3.2:1b for the zero-shot evaluation. As a next step I would try to test with a larger data set.

Potential issues with data:

-The data was created synthetically using gemini, so there can be inaccuracies in the descriptions I may have missed

-Data only includes 50 questions which is relatively small

-Some basketball schemes and plays have multiple names

### Player Stats Questions

| Model | Setting | Tools | Accuracy | Std Error |
|-------|---------|-------|----------|-----------|
| llama3.2 | Zero-shot | No | 0.080 | 0.055 |
| llama3.2 | Few-shot | No | 0.240 | 0.087 |
| llama3.2 | Zero-shot | Yes | 1.000 | 0.000 |
| llama3.2 | Few-shot | Yes | 1.000 | 0.000 |
| llama3.2:1b | Zero-shot | No | 0.040 | 0.040 |
| llama3.2:1b | Few-shot | No | 0.040 | 0.040 |
| llama3.2:1b | Zero-shot | Yes | 0.040 | 0.040 |
| llama3.2:1b | Few-shot | Yes | 0.040 | 0.040 |