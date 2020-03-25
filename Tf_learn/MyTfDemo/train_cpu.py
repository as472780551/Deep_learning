import tensorflow as tf
from multi_input_data import get_data
import Const as C
import model as m
# 设置GPU按需增长
config = tf.ConfigProto()
#config.gpu_options.allow_growth = True
sess = tf.Session(config=config)

def get_loss(train_next_element,p1,p2,p3,label,mse,train_step):
    p1_run, p2_run, p3_run, label_run = sess.run([train_next_element[0],
                                                  train_next_element[1],
                                                  train_next_element[2],
                                                  train_next_element[3]])
    # 注意mse_loss不要和右边的mse重名，要不然报错
    mse_loss, _ = sess.run([mse, train_step], feed_dict={
        p1: p1_run,
        p2: p2_run,
        p3: p3_run,
        label: label_run
    })
    return mse_loss



def train_on_cpu():

    p1 = tf.placeholder(tf.float32, [None, 20, 40, 3])
    p2 = tf.placeholder(tf.float32, [None, 8, 10])
    p3 = tf.placeholder(tf.float32, [None, 10])
    label = tf.placeholder(tf.float32,[None,1])
    y_pred = m.MyNet(p1,p2,p3)

    #mse = tf.reduce_sum((label -y_pred)**2)
    mse = tf.losses.mean_squared_error(label, y_pred)
    #mse = tf.nn.l2_loss(label,y_pred)
    train_step = tf.train.AdamOptimizer(1e-4).minimize(mse)

    sess.run(tf.global_variables_initializer())
    # Compute for epochs.
    all_steps = 0
    for i in range(C.EPOCHS):
        train_next_element = get_data(C.TRAIN_RECODER_PATH)
        test_next_element = get_data(C.TEST_RECODER_PATH)
        train_bacth_per_epoch = 0
        while True:
            try:
                train_bacth_per_epoch+=1
                all_steps+=1
                train_mse_loss = get_loss(train_next_element,p1, p2, p3, label, mse, train_step)
                print("Train Epoch {} Batch {} All steps {}: MSE ==> {}".format(i + 1, train_bacth_per_epoch,all_steps, train_mse_loss))
            except tf.errors.OutOfRangeError:
                break

        test_loss = 0
        test_batchs = 0
        while True:
            try:
                test_mse_loss = get_loss(test_next_element, p1, p2, p3, label, mse, train_step)
                test_loss += test_mse_loss
                test_batchs += 1
                print("Test batch {} : MSE ==> {}".format(test_batchs, test_mse_loss))
            except tf.errors.OutOfRangeError:
                break
        test_loss_ave = test_loss / test_batchs
        print("Epoch {} : All Test Data Average MSE {}".format(i+1,test_loss_ave))





if __name__ == '__main__':
    train_on_cpu()










