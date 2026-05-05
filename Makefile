default: ms.pdf

ms.pdf: ms.qmd
	quarto render "ms.qmd" --to pdf


