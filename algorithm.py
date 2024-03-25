def ocr_img(images: list, remote=False):
    """
    识别多张图片，如果remote=True，则下载远程图片，如果remote=False，则直接将图片对象传入
    :param images: 图片列表
    :param remote: 释放远程
    :return:
    """
    try:
        result = []
        for i in range(0, len(images), 5):
            _img_paths = images[i: 1 + 5]
            ocr_model = get_ocr_model()
            print('ocr_model',ocr_model)
            img_paths = []
            if remote:
                for url in _img_paths:
                    img_name = download_img(url)
                    if not img_name:
                        continue
                    img_paths.append(img_name)
            else:
                for img in images:
                    img_name = str(int(time.time())) + '.jpg'
                    save_img(img_name, img)
                    img_paths.append(img_name)
            imgs = []
            for img in img_paths:
                img_name = handle_img(img)
                # 兼容中文路径
                # img = cv2.imdecode(np.fromfile(os.path.join(images_path, img_name), dtype=np.uint8), -1)
                img = cv2.imread(os.path.join(images_path, img_name))
                imgs.append(img)
            result.extend(ocr_model.recognize_text(images=imgs))
        return result
    except Exception as e:
        logger.error(f"OCR Model处理失败, error: {e}", exc_info=True)
        return []

def get_ocr_model():
    """手动GC，控制model使用内存"""

    global OCR_MODEL_USER_TIMES
    global OCRModel
    module_name = "chinese_ocr_db_crnn_server"
    # 使用10次，就释放模型
    if OCR_MODEL_USER_TIMES < 10:
        if not OCRModel:
            OCRModel = hub.Module(name=module_name)
        OCR_MODEL_USER_TIMES += 1
    else:
        del OCRModel
        gc.collect()
        OCRModel = hub.Module(name=module_name)
        OCR_MODEL_USER_TIMES = 0
    return OCRModel
