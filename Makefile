test:
	pytest --ignore gosling/examples --doctest-modules gosling

clean-generated:
	rm -rf doc/_build
	rm -rf doc/user_guide/generated/
	rm -rf doc/gallery

.PHONY: doc
doc:
	sphinx-build -b html doc dist
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."
