var app = new Vue({
    el: '#app',
    data: {
        width: 600,
        height: 500,
        tagsNum: 20,
        RADIUS: 200,
        speedX: Math.PI / 360,
        speedY: Math.PI / 360,
        input: '',
        tags: [],
        //获取屏幕宽度，如果小于768，就100%
        isMobile: document.documentElement.clientWidth < 768
    },
    computed: {
		CX() {
            if (this.isMobile) {
                return (this.width / 2)/2.2
            } else {
                return (this.width / 2/1.15);
            }
        },
        CY() {
            return this.height / 2;
        }
    },
    created() {
        //给个默认的标签显示
        this.search('人工智能');

    },
    mounted() {//使球开始旋转
        setInterval(() => {
            this.rotateX(this.speedX);
            this.rotateY(this.speedY);
        }, 17)
    },
    methods: {
        enter() {
            // this.search(this.input);
            if (this.input) {
                window.location.href = '/knowledge.html?word=' + this.input;
            }
        },
        search(val) {
            if (val == "") {
                //空的，什么也不做
                return;
            }
            if (val) {
                this.input = val;
            }
            this.tags = [];
            var self = this;

			var data = [["白血病"], ["百日咳"], ["乙肝"], ["肺癌"], ["苯中毒"], ["铅中毒"], ["水中毒"], ["手足口病"], ["周龙超炎症"], ["糖尿病"],["白内障"], ["肾衰竭"], ["皮疹"], ["肾结石"], ["伤风感冒"],["狂犬病"], ["淋巴癌"], ["骨癌"], ["阑尾炎"], ["皮囊炎"],["湿疹"], ["皮肤过敏"], ["冠心病"], ["高血压"], ["心肌梗塞"],["牛皮癣"], ["银屑病"], ["破伤风"], ["肝硬化"], ["抑郁症"]]
			let len = data.length;
			for (let i = 0; i < len; i++) {
				let tag = {};
				let k = -1 + (2 * (i + 1) - 1) / len;
				let a = Math.acos(k);
				let b = a * Math.sqrt(len * Math.PI)
				let txt = data[i][0];
				let temp = txt.match(new RegExp("\\[(.| )+?\\]", "igm"));
				if (temp) {
					txt = temp[0].replace(/\[|\]/g, "");
				}
				tag.text = txt;
				tag.x = this.CX + this.RADIUS * Math.sin(a) * Math.cos(b);
				tag.y = this.CY + this.RADIUS * Math.sin(a) * Math.sin(b);
				tag.z = this.RADIUS * Math.cos(a);
				//颜色随机
				tag.color = "rgb(" + parseInt(Math.random() * 255) + "," + parseInt(Math.random() * 255) + "," + parseInt(Math.random() * 255) + ")";
				//访问地址
				// tag.href = '/knowledge.html?word=' + tag.text;
				tag.href = '/knowledge.html?word=' + txt;
				self.tags.push(tag)
			}

			
            // //这里替换api地址
            // axios.get('https://api.ownthink.com/kg/ambiguous?mention=' + this.input).then(res => {
                // var data = res.data.data;
                // let len = data.length;
                // for (let i = 0; i < len; i++) {
                    // let tag = {};
                    // let k = -1 + (2 * (i + 1) - 1) / len;
                    // let a = Math.acos(k);
                    // let b = a * Math.sqrt(len * Math.PI)
                    // let txt = data[i][0];
                    // let temp = txt.match(new RegExp("\\[(.| )+?\\]", "igm"));
                    // if (temp) {
                        // txt = temp[0].replace(/\[|\]/g, "");
                    // }
                    // tag.text = txt;
                    // tag.x = this.CX + this.RADIUS * Math.sin(a) * Math.cos(b);
                    // tag.y = this.CY + this.RADIUS * Math.sin(a) * Math.sin(b);
                    // tag.z = this.RADIUS * Math.cos(a);
                    // //颜色随机
                    // tag.color = "rgb(" + parseInt(Math.random() * 255) + "," + parseInt(Math.random() * 255) + "," + parseInt(Math.random() * 255) + ")";
                    // //访问地址
                    // // tag.href = '/knowledge.html?word=' + tag.text;
                    // tag.href = '/knowledge.html?word=' + txt;
                    // self.tags.push(tag)
                // }
            // });
        },
        rotateX(speedX) {
            var cos = Math.cos(speedX);
            var sin = Math.sin(speedX);
            for (let tag of this.tags) {
                var y1 = (tag.y - this.CY) * cos - tag.z * sin + this.CY;
                var z1 = tag.z * cos + (tag.y - this.CY) * sin;
                tag.y = y1;
                tag.z = z1;
            }
        },
        rotateY(speedY) {
            var cos = Math.cos(speedY);
            var sin = Math.sin(speedY);
            for (let tag of this.tags) {
                var x1 = (tag.x - this.CX) * cos - tag.z * sin + this.CX;
                var z1 = tag.z * cos + (tag.x - this.CX) * sin;
                tag.x = x1;
                tag.z = z1;
            }
        },
        listener(event) {//响应鼠标移动
            var x = event.clientX - this.CX;
            var y = event.clientY - this.CY;
            this.speedX = x * 0.0001 > 0 ? Math.min(this.RADIUS * 0.00002, x * 0.0001) : Math.max(-this.RADIUS * 0.00002, x * 0.0001);
            this.speedY = y * 0.0001 > 0 ? Math.min(this.RADIUS * 0.00002, y * 0.0001) : Math.max(-this.RADIUS * 0.00002, y * 0.0001);
        }
    }
})

