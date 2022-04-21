use openh264::decoder::Decoder;

#[no_mangle]
extern "C" fn decode(in_buffer: *mut u8, in_length: usize, out_buffer: *mut u8, out_length: usize) -> usize {
    let bytes = unsafe { std::slice::from_raw_parts_mut(in_buffer, in_length) };
    let out = unsafe { std::slice::from_raw_parts_mut(out_buffer, out_length) };
    let mut decoder = Decoder::new().unwrap();
    let yuv_result = decoder.decode(&bytes[..]);
    if yuv_result.is_err() {
        return 0;
    }
    let yuv = yuv_result.unwrap();
    let dim = yuv.dimension_rgb();
    let rgb_len = dim.0 * dim.1 * 3;
    let tgt = &mut out[0..rgb_len];
    let result = yuv.write_rgb8(tgt);
    if result.is_err() {
        return 0;
    }
    result.unwrap();
    return rgb_len;
}