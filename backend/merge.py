def merge_files(files, title_sep=" ", content_sep="\n"):
    titles = []
    contents = []
    for file in files or []:
        title = file.get("name")
        content = file.get("content")

        if title is not None:
            titles.append(str(title))
        if content is not None:
            contents.append(str(content))

    merged_title = title_sep.join(titles)
    merged_content = content_sep.join(contents)

    return {"title": merged_title, "content": merged_content}